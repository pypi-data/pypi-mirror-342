import time
from typing import Optional, List

import os
import re
import builtins
import inspect
import requests

import gymnasium as gym
import numpy as np
import tensorflow as tf
import torch

from rich.align import Align
from rich.text import Text
from rich.syntax import Syntax

from sai_rl.api.client import APIClient
from sai_rl.sai_console import SAIConsole, SAIStatus
from sai_rl.error import ActionFunctionError, NetworkError

from sai_rl.action_function.action_function import ActionFunction
from sai_rl.types import ModelType, ModelLibraryType


# Blacklist of potentially unsafe builtins
UNSAFE_BUILTINS = {
    # System operations
    "exec",
    "eval",
    "compile",
    # File operations
    "open",
    "file",
    "__import__",
    # Process operations
    "system",
    "subprocess",
    # Other potentially dangerous operations
    "globals",
    "locals",
    "vars",
    "breakpoint",
    "exit",
    "quit",
}

# Create safe_globals dynamically
safe_builtins = {
    name: getattr(builtins, name)
    for name in dir(builtins)
    if name not in UNSAFE_BUILTINS
    and not name.startswith("_")  # Exclude private methods
}
# Add back specific private builtins that we need
safe_builtins["__build_class__"] = builtins.__build_class__

safe_globals = {
    "__builtins__": safe_builtins,
    "__name__": "__main__",
    "__file__": "<string>",
    "__doc__": None,
    # External libraries
    "np": np,
    "tf": tf,
    "torch": torch,
    "ActionFunction": ActionFunction,
}


class ActionFunctionManager:
    def __init__(
        self,
        api: APIClient,
        console: SAIConsole,
        path: Optional[str] = None,
        download_path: Optional[str] = "~/.sai/temp",
        status: Optional[SAIStatus] = None,
    ):
        self._api = api
        self._console = console
        self._action_class: Optional[ActionFunction] = None

        self._id = None
        self._path = None
        self._download_path = download_path

        self.load(path, status=status)

    def load(
        self,
        path: Optional[str] = None,
        id: Optional[str] = None,
        no_print: bool = False,
        status: Optional[SAIStatus] = None,
    ):
        if status:
            status.update(f"Loading action function from {path}")

        self.reset()

        if not path:
            return

        if path.startswith(("http://", "https://")):
            self._load_from_url(path, status=status, id=id)
        elif path.endswith((".py")) and os.path.exists(path):
            self._load_local(path, status=status)
        elif len(path) == 12:
            self._load_from_platform(path, status=status)
        else:
            raise ActionFunctionError(f"Unsupported action function path: {path}")

        if not no_print:
            self._print(status=status)
            self._console.success("Successfully loaded action function.")

    def _print(self, status: Optional[SAIStatus] = None):
        if status:
            status.update("Processing action function...")

        title = f"Action Function: {self.name}"
        info_group = f"""[bold cyan]ID:[/bold cyan]          {self._id if self._id else "N/A"}
[bold cyan]Name:[/bold cyan]        {self.name}
[bold cyan]Model Types:[/bold cyan]  {self.model_type}"""

        if not self._path:
            self._console.error("Action function is not loaded")
            return

        panel_group = self._console.group(
            Align.left(Text.from_markup(info_group)),
            Text.from_markup("[bold cyan]\nCode:[/bold cyan]\n"),
            Syntax.from_path(self._path, theme="github-dark"),
        )

        panel = self._console.panel(panel_group, title=title, padding=(1, 2))
        self._console.print()
        self._console.print(panel)

    def _load_local(self, path: str, status: Optional[SAIStatus] = None):
        self._path = path

    def _load_from_platform(self, id: str, status: Optional[SAIStatus] = None):
        self._id = id

        if status:
            status.update(f"Fetching action function from platform: {id}")
        action_fn = self._api.action_function.get(id)

        if not action_fn:
            raise ActionFunctionError(f"Failed to fetch action function: {id}")

        self._load_from_url(action_fn.get("download_url"), status=status)

    def _load_from_url(
        self, url: str, status: Optional[SAIStatus] = None, id: Optional[str] = None
    ):
        self._path = self._download(url, status=status, id=id)
        self._action_class = self.get()

    def _download(
        self, url: str, status: Optional[SAIStatus] = None, id: Optional[str] = None
    ):
        if status:
            status.update("Downloading action function...")
            status.stop()

        if not self._download_path:
            raise ActionFunctionError("Download path not set")

        os.makedirs(self._download_path, exist_ok=True)
        filename = id if id else f"{time.time()}"
        action_path = f"{self._download_path}/{filename}.py"

        if os.path.exists(action_path):
            os.remove(action_path)

        try:
            with self._console.progress("Downloading action function") as progress:
                with requests.get(url, stream=True) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get("content-length", 0))
                    task = progress.add_task("Downloading...", total=total_size)

                    chunk_size = 8192  # 8 KB
                    downloaded_size = 0

                    with open(action_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                downloaded_size += len(chunk)
                                progress.update(task, advance=len(chunk))

        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Failed to download action function: {e}")
        finally:
            if status:
                status.start()

        return action_path

    def submit(self, status: Optional[SAIStatus] = None):
        if not self.is_loaded:
            raise ActionFunctionError("Action function is not loaded")

        if not self.is_local:
            raise ActionFunctionError("Action function has already been submitted")

        if not self.name:
            raise ActionFunctionError("Action function name not set")

        if not self.model_type:
            raise ActionFunctionError("Action function model type not set")

        try:
            result = self._api.action_function.submit(
                name=self.name,
                compatible_types=[model_type for model_type in self.model_type],
            )

            if not result:
                raise ActionFunctionError("Failed to create action function")

            if status:
                status.update("Uploading action function...")
                status.stop()

            if not self._path:
                raise ActionFunctionError("Action function path not set")

            with open(self._path, "rb") as action_file:
                file_size = os.path.getsize(self._path)
                with self._console.progress("Uploading action function...") as p:
                    task = p.add_task("Uploading", total=file_size)
                    upload_response = requests.put(
                        result["upload_url"], data=action_file
                    )
                    upload_response.raise_for_status()
                    p.update(task, completed=file_size)

            if status:
                status.start()

            self._id = result["action_function"]["id"]
            self.load(
                path=result["action_function"]["download_url"],
                status=status,
                id=result["action_function"]["id"],
                no_print=True,
            )

            self._console.success(f"Submitted action function: {self.name}")

            return result["action_function"]

        except Exception as e:
            raise ActionFunctionError(f"Failed to submit action function: {str(e)}")

    def reset(self):
        self._action_class = None
        self._id = None
        self._path = None

    @staticmethod
    def remove_imports(code_string: str) -> str:
        """Remove import statements from code for security."""
        pattern = re.compile(
            r"^\s*#?\s*(from\s+\w+\s+import\s+.*|import\s+\w+.*|from\s+\w+\s+import\s+\(.*\)|import\s+\(.*\))",
            re.MULTILINE,
        )
        return re.sub(pattern, "", code_string)

    @property
    def is_local(self) -> bool:
        return self._action_class is None and self.is_loaded

    @property
    def is_loaded(self) -> bool:
        return self._path is not None

    @property
    def name(self) -> Optional[str]:
        if self._action_class:
            return self._action_class.name

        if self.is_loaded:
            return self.get().name

        return None

    @property
    def id(self) -> Optional[str]:
        return self._id

    @property
    def model_type(self) -> Optional[List[ModelLibraryType]]:
        if not self.is_loaded:
            return None

        if self._action_class:
            model_type = self._action_class.model_type
        else:
            model_type = self.get().model_type

        if isinstance(model_type, (str, ModelLibraryType)):
            return [model_type]
        return model_type

    def get(self) -> Optional[ActionFunction]:
        """Load action function class from file with security measures."""

        if self._action_class:
            return self._action_class

        if not self._path:
            return None

        try:
            with open(self._path, "r") as f:
                code = f.read()

            clean_code = self.remove_imports(code)
            namespace = dict(safe_globals)
            exec(clean_code, namespace)

            action_classes = [
                obj
                for name, obj in namespace.items()
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, ActionFunction)
                    and obj != ActionFunction
                )
            ]

            if not action_classes:
                raise ActionFunctionError("No ActionFunction subclass found in file")
            if len(action_classes) > 1:
                raise ActionFunctionError(
                    "Multiple ActionFunction classes found in file"
                )

            return action_classes[0]

        except Exception as e:
            raise ActionFunctionError(f"Error loading action function: {e}")

    def verify_compliance(
        self,
        env: gym.Env,
        model: ModelType,
        model_type: ModelLibraryType,
        status: Optional[SAIStatus] = None,
    ):
        if status:
            status.update("Verifying action function compliance")

        try:
            action_class = self.get()
            if not action_class:
                raise ActionFunctionError("Action function is not loaded")

            required_attrs = ["name", "model_type"]
            for attr in required_attrs:
                if not hasattr(action_class, attr):
                    raise ActionFunctionError(f"Missing required attribute: {attr}")

            action_function = action_class()
            if hasattr(env, "action_space"):
                action_function.add_action_space(env.action_space)            

            model_types = action_function.model_type
            if isinstance(model_types, str):
                model_types = [model_types]

            if model_type and model_type not in model_types:
                raise ActionFunctionError(
                    f"Model type {model_type} not in {model_types}"
                )

            obs = env.observation_space.sample()
            action = action_function.get_action(model, obs)

            if not isinstance(action, (int, np.int32, np.int64, np.ndarray)):
                raise ActionFunctionError(f"Invalid action type: {type(action)}")

            if not env.action_space.contains(action):
                raise ActionFunctionError(f"Action {action} not in action space")

            return True

        except Exception as e:
            raise ActionFunctionError(f"Compliance check failed: {e}")
