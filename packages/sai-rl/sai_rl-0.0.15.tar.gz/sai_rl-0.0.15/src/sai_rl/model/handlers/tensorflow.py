import tensorflow as tf
import keras

from sai_rl.model.handlers.base_handler import BaseModelHandler
from sai_rl.model.exporting import tf_to_onnx


class TensorFlowModelHandler(BaseModelHandler):
    def load_model(self, model_path):
        return keras.models.load_model(model_path)

    def get_action(self, model, obs):
        actions = model.predict(obs[None, :])
        return tf.argmax(actions, axis=1).numpy()[0]

    def save_model(self, model, model_path):
        model.save(model_path)

    def export_to_onnx(self, model, env, path):
        return tf_to_onnx(model, env, path)
