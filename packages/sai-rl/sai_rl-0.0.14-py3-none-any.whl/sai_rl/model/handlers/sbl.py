import stable_baselines3 as sb3

from sai_rl.model.handlers.base_handler import BaseModelHandler
from sai_rl.model.exporting import sb3_to_onnx


class SBL3ModelHandler(BaseModelHandler):
    def __init__(self, model_class="PPO"):
        self.model_class = getattr(sb3, model_class)

    def load_model(self, model_path):
        return self.model_class.load(model_path)

    def get_action(self, model, obs):
        action, _states = model.predict(obs)
        return action

    def save_model(self, model, model_path):
        model.save(model_path)

    def export_to_onnx(self, model, env, path):
        return sb3_to_onnx(model, env, path)
