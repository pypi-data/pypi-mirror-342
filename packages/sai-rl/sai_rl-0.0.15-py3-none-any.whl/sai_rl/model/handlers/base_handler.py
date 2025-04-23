from abc import ABC, abstractmethod

import numpy as np


class BaseModelHandler(ABC):
    @abstractmethod
    def load_model(self, model_path: str):
        pass

    @abstractmethod
    def get_action(self, model, obs: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def save_model(self, model, model_path: str):
        pass

    @abstractmethod
    def export_to_onnx(self, model, env, path: str):
        pass
