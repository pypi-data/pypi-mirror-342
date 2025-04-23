import numpy as np

from tensorweaver.layers.layer import Layer
from tensorweaver.parameter import Parameter


class Linear(Layer):
    def __init__(self, in_features: int, out_features: int, bias: bool = True, dtype=None):
        super().__init__()

        self.out_dim = out_features
        self.in_dim = in_features
        self.bias = bias

        self._init_parameters()

    def _init_parameters(self):
        # Xavier/Glorot initialization
        bound = np.sqrt(6.0 / (self.in_dim + self.out_dim))
        self.weight = Parameter(
            np.random.uniform(-bound, bound, (self.in_dim, self.out_dim)), name="weight"
        )

        self.bias_weight = None
        if self.bias:
            self.bias_weight = Parameter(np.zeros(self.out_dim), name="bias")  # Initialize bias to zeros

    def forward(self, x):
        output = x @ self.weight

        if self.bias:
            output = output + self.bias_weight

        return output
