from abc import ABC, abstractmethod
from typing import Any, Union
import numpy as np
import torch
import tensorflow as tf

from ..types import ModelType, ModelLibraryType, StateType


class ActionFunction(ABC):
    """Base class for custom action functions in the Arena platform.

    Inherit from this class to create your own custom action function.
    Example:
        ```python
        class MyActionFunction(ActionFunction):
            model_type = "pytorch"

            def preprocess_state(self, state):
                if len(state.shape) < 2:
                    return self.expand_dims(state, 0)
                return state

            def get_action(self, model, state):
                state = self.preprocess_state(state)
                state = self.to_tensor(state).float()

                with torch.no_grad():
                    policy = model(state)

                return int(self.to_numpy(policy).argmax())
        ```
    """

    name: str = "BaseActionFunction"
    model_type: Union[ModelLibraryType, list[ModelLibraryType], None] = None
    action_space = None

    # Helper methods for state conversion
    def to_numpy(self, x: Any) -> np.ndarray:
        """Convert input to numpy array."""
        if isinstance(x, torch.Tensor):
            return x.detach().cpu().numpy()
        if isinstance(x, tf.Tensor):
            return x.numpy()
        return np.array(x)

    def to_tensor(self, x: Any) -> torch.Tensor:
        """Convert input to PyTorch tensor."""
        if isinstance(x, torch.Tensor):
            return x
        if isinstance(x, tf.Tensor):
            return torch.from_numpy(x.numpy())
        return torch.from_numpy(np.array(x))

    def to_tf_tensor(self, x: Any) -> tf.Tensor:
        """Convert input to TensorFlow tensor."""
        if isinstance(x, tf.Tensor):
            return x
        if isinstance(x, torch.Tensor):
            return tf.convert_to_tensor(self.to_numpy(x))
        return tf.convert_to_tensor(x)

    def expand_dims(self, x: Any, axis: int) -> Any:
        """Add dimension to input at specified axis."""
        if isinstance(x, torch.Tensor):
            return torch.unsqueeze(x, axis)
        if isinstance(x, tf.Tensor):
            return tf.expand_dims(x, axis)
        return np.expand_dims(x, axis)

    def add_action_space(self, action_space):
        """Add action space for more advanced custom actions."""
        self.action_space = action_space

    @abstractmethod
    def get_action(self, model: ModelType, obs: StateType):
        """Convert model output to action.

        Args:
            model: The loaded ML model
            state: The environment observation/state

        Returns:
            int: The selected action
        """
        raise NotImplementedError

    def preprocess_state(self, obs: StateType) -> StateType:
        """Optional preprocessing of state before model inference.

        Override this method if you need custom state preprocessing.
        """
        return obs

    def postprocess_action(self, action: Any):
        """Optional postprocessing of action after model inference.

        Override this method if you need custom action postprocessing.
        """
        return int(action)
