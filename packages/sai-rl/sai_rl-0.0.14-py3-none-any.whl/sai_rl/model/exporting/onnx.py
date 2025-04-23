import torch
import onnx
import tf2onnx
import tensorflow as tf

sb3_softmax_classes = ["PPO", "A2C", "SAC"]

q_network_classes = ["DQN"]


class SB3ExportingWrapper(torch.nn.Module):
    def __init__(self, model):
        super(SB3ExportingWrapper, self).__init__()
        self.name = model.__class__.__name__
        self.policy = model.policy

    def forward(self, state):
        if self.name in sb3_softmax_classes:
            latent_pi, _ = self.policy.mlp_extractor(state)
            action_dist = self.policy._get_action_dist_from_latent(latent_pi)
            return torch.nn.functional.softmax(action_dist.distribution.logits, dim=-1)
        elif self.name in q_network_classes:
            return self.policy.q_net(state)
        else:
            return self.policy.forward(state)


def torch_to_onnx(model, env, path="model"):
    # Temporarily remove the train method for export
    original_train = model.train
    model.train = lambda *args, **kwargs: None

    # Create input to validate model
    torch_input = torch.from_numpy(env.observation_space.sample()).float()
    torch_input = torch_input.unsqueeze(0)
    torch.onnx.export(
        model,
        torch_input,
        path if path.endswith(".onnx") else f"{path}.onnx",
        input_names=["input"],
        output_names=["output"],
    )

    # Restore training method
    model.train = original_train


def sb3_to_onnx(model, env, path="model"):
    torch_to_onnx(SB3ExportingWrapper(model), env, path)


def tf_to_onnx(model_output_fn, env, path="model"):
    model_output_fn.output_names = ["output"]
    input_signature = [
        tf.TensorSpec(
            [None, *env.observation_space.sample().shape], tf.float32, name="input"
        )
    ]
    onnx_model, _ = tf2onnx.convert.from_keras(
        model_output_fn, input_signature, opset=13
    )
    onnx.save(onnx_model, path if path.endswith(".onnx") else f"{path}.onnx")
