import gymnasium as gym

from sai_rl.error import ModelError
from sai_rl.types import ModelLibraryType

from sai_rl.model.handlers.base_handler import BaseModelHandler
from sai_rl.model.handlers.pytorch import PyTorchModelHandler
from sai_rl.model.handlers.tensorflow import TensorFlowModelHandler
from sai_rl.model.handlers.sbl import SBL3ModelHandler
from sai_rl.model.handlers.onnx import OnnxModelHandler


def get_handler(env: gym.Env, model_type: ModelLibraryType) -> BaseModelHandler:
    handlers = {
        "pytorch": PyTorchModelHandler(),
        "tensorflow": TensorFlowModelHandler(),
        "stable_baselines3": SBL3ModelHandler(),
        "onnx": OnnxModelHandler(env),
    }
    handler = handlers.get(model_type)

    if handler is None:
        raise ModelError(f"Unsupported model type: {model_type}")

    return handler
