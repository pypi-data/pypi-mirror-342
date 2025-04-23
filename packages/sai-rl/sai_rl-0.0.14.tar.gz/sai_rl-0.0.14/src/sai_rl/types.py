from typing import Union, Literal, TypeAlias

import numpy as np
import torch
import keras
import tensorflow as tf
from stable_baselines3.common.base_class import BaseAlgorithm

ModelType: TypeAlias = Union[
    str, torch.nn.Module, keras.Model, BaseAlgorithm, "OnnxAgentWrapper"  # noqa: F821 # type: ignore
]

ModelLibraryType: TypeAlias = Literal[
    "pytorch", "tensorflow", "stable_baselines3", "onnx"
]

StateType: TypeAlias = Union[np.ndarray, torch.Tensor, tf.Tensor]
