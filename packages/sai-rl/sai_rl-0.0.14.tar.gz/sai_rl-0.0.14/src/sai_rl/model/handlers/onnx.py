import numpy as np
import onnxruntime

from sai_rl.model.handlers.base_handler import BaseModelHandler


class OnnxAgentWrapper:
    def __init__(self, env, path):
        self.tensor_dims = len(env.observation_space.sample().shape) + 1
        self.sess = onnxruntime.InferenceSession(
            path, providers=["CPUExecutionProvider"]
        )

    def forward(self, state):
        if len(state.shape) < self.tensor_dims:
            state = np.expand_dims(state, axis=0)
        return self.sess.run(None, {"input": state})


class OnnxModelHandler(BaseModelHandler):
    def __init__(self, env):
        self.env = env

    def load_model(self, model_path):
        return OnnxAgentWrapper(self.env, model_path)

    def get_action(self, model, obs):
        output = model.forward(obs.astype(np.float32))
        return np.argmax(output)

    def save_model(self, model, model_path):
        model.save(model_path)

    def export_to_onnx(self, model, _, path):
        return self.save_model(model, path)
