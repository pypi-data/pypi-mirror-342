import torch

from sai_rl.model.handlers.base_handler import BaseModelHandler
from sai_rl.model.exporting import torch_to_onnx


class PyTorchModelHandler(BaseModelHandler):
    def load_model(self, model_path):
        return torch.jit.load(model_path)

    def get_action(self, model, obs):
        obs_tensor = torch.tensor(obs[None, :], dtype=torch.float32)
        actions = model(obs_tensor)
        return torch.argmax(actions).item()

    def save_model(self, model, model_path):
        torch.jit.save(model, model_path)

    def export_to_onnx(self, model, env, path):
        return torch_to_onnx(model, env, path)
