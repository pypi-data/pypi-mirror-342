from typing import Optional

import keras
import torch

from stable_baselines3.common.base_class import BaseAlgorithm

import os
import requests
import gymnasium as gym

from rich.align import Align
from rich.text import Text

from sai_rl.sai_console import SAIConsole, SAIStatus
from sai_rl.utils import config
from sai_rl.error import ModelError, NetworkError
from sai_rl.types import ModelType, ModelLibraryType

from sai_rl.model.handlers import OnnxAgentWrapper, get_handler
from sai_rl.action_function.action_manager import ActionFunctionManager


class ModelManager:
    def __init__(
        self,
        console: SAIConsole,
        env: gym.Env,
        model: ModelType,
        model_type: Optional[ModelLibraryType] = None,
        action_manager: Optional[ActionFunctionManager] = None,
        download_dir: str = config.temp_path,
        status: Optional[SAIStatus] = None,
    ):
        if status is not None:
            status.update("Loading model...")

        self._console = console
        self._env = env

        self._download_dir = download_dir

        self._model_type = self._determine_model_type(model, model_type, status)
        self._model, self._handler = self._load_model(model, status)

        self._action_function = None
        self._action_manager = action_manager
        if action_manager and action_manager.is_loaded:
            self._action_manager.verify_compliance(
                self._env, self._model, self._model_type, status
            )
            self._action_function = self._action_manager.get()()
            if hasattr(env, "action_space"):
                self._action_function.add_action_space(env.action_space)

        self._print(status=status)

        if self._action_function:
            self._console.success("Action function compliance check passed.")
        self._console.success("Successfully loaded model.")

    def _determine_model_type(
        self,
        model: ModelType,
        model_type: Optional[ModelLibraryType],
        status: Optional[SAIStatus] = None,
    ) -> ModelLibraryType:
        determined_model_type = None
        self._console.debug(f"Determining model type for {model}")
        if status is not None:
            status.update("Determining model type for model...")

        if isinstance(model, str):
            if model.startswith(("http://", "https://")):
                if model_type is None:
                    raise ModelError("model_type must be provided for URL models.")
                determined_model_type = model_type
            elif os.path.exists(model):
                determined_model_type = self._determine_file_type(model)
            else:
                raise ModelError(f"Invalid model path or URL: {model}")
        elif isinstance(model, torch.nn.Module):
            determined_model_type = "pytorch"
        elif isinstance(model, keras.Model):
            determined_model_type = "tensorflow"
        elif isinstance(model, BaseAlgorithm):
            determined_model_type = "stable_baselines3"
        elif isinstance(model, OnnxAgentWrapper):
            determined_model_type = "onnx"
        elif model_type:
            determined_model_type = model_type
        else:
            raise ModelError("Unsupported model type")

        if model_type and determined_model_type != model_type:
            raise ModelError(
                f"Provided model_type '{model_type}' does not match detected type '{determined_model_type}'"
            )

        self._console.debug(f"Determined model type: {determined_model_type}")
        return determined_model_type

    def _determine_file_type(self, file_path: str) -> ModelLibraryType:
        _, ext = os.path.splitext(file_path)
        if ext in [".pt", ".pth"]:
            return "pytorch"
        elif ext in [".h5", ".keras"]:
            return "tensorflow"
        elif ext == ".zip":
            return "stable_baselines3"
        elif ext == ".onnx":
            return "onnx"
        else:
            raise ModelError(f"Unsupported file type: {ext}")

    def _load_model(self, model: ModelType, status: Optional[SAIStatus] = None):
        self._console.debug(f"Loading model: {model}")
        loaded_model = None
        loaded_handler = None

        if isinstance(model, str) and model.startswith(("http://", "https://")):
            model_path = self._download_model(model, status)
            if status is not None:
                status.update("Loading model...")
                status.stop()
            loaded_handler = get_handler(self._env, self._model_type)
            loaded_model = loaded_handler.load_model(model_path)

        elif self._model_type in ["pytorch", "tensorflow", "stable_baselines3", "onnx"]:
            loaded_handler = get_handler(self._env, self._model_type)
            if isinstance(model, str):
                if status is not None:
                    status.update("Loading model...")
                    status.stop()
                loaded_model = loaded_handler.load_model(model)
            else:
                loaded_model = model
        else:
            raise ModelError(f"Unsupported model type: {self._model_type}")

        if status is not None:
            status.start()

        self._console.debug(
            f"Loaded model: {loaded_model} with handler: {loaded_handler}"
        )
        return loaded_model, loaded_handler

    def _download_model(self, model_url: str, status: Optional[SAIStatus] = None):
        self._console.debug(f"Downloading model from {model_url}")

        if status is not None:
            status.update("Downloading model...")
            status.stop()

        os.makedirs(self._download_dir, exist_ok=True)
        filename = model_url.split("/")[-1].split("?")[0]
        file_extension = {
            "stable_baselines3": ".zip",
            "pytorch": ".pt",
            "tensorflow": ".keras",
            "onnx": ".onnx",
        }.get(self._model_type, "")
        model_path = os.path.join(self._download_dir, filename + file_extension)

        try:
            with self._console.progress("Downloading model") as progress:
                with requests.get(model_url, stream=True) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get("content-length", 0))
                    task = progress.add_task("[green]Downloading...", total=total_size)

                    chunk_size = 8192  # 8 KB
                    downloaded_size = 0

                    with open(model_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                downloaded_size += len(chunk)
                                progress.update(task, advance=len(chunk))

        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Failed to download model: {e}")

        if status is not None:
            status.start()

        return model_path

    def _print(self, status: Optional[SAIStatus] = None):
        if status:
            status.update("Processing model...")

        title = "Model"
        info_group = f"""[bold cyan]Type:[/bold cyan]          {self._model_type}
[bold cyan]Action Function:[/bold cyan]  {self._action_function.name if self._action_function else "N/A"}
[bold cyan]Environment:[/bold cyan]    {self._env.spec.id}"""

        panel_group = self._console.group(
            Align.left(Text.from_markup(info_group)),
        )

        panel = self._console.panel(panel_group, title=title, padding=(1, 2))
        self._console.print()
        self._console.print(panel)

    def get_action(self, obs):
        if self._action_function:
            return self._action_function.get_action(self._model, obs)
        else:
            return self._handler.get_action(self._model, obs)

    def save_model(self, model_path, use_onnx=False):
        if use_onnx:
            self._handler.export_to_onnx(self._model, self._env, model_path)
        else:
            self._handler.save_model(self._model, model_path)

    @property
    def model_type(self):
        return self._model_type

    @property
    def model(self):
        return self._model
