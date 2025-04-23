from tensorweaver.autodiff.function import Function
from tensorweaver.autodiff.helpers import as_variable

import numpy as np

from tensorweaver.autodiff.variable import Variable


def np_sum_to(x, shape):
    # copied from dezero
    if isinstance(x, Variable):
        x = x.data
    ndim = len(shape)
    lead = x.ndim - ndim
    lead_axis = tuple(range(lead))

    axis = tuple([i + lead for i, sx in enumerate(shape) if sx == 1])
    y = x.sum(lead_axis + axis, keepdims=True)
    if lead > 0:
        y = y.squeeze(lead_axis)
    return y


class SumTo(Function):
    def __init__(self, target_shape):
        super().__init__()

        self.target_shape = target_shape
        self.original_shape = None

    def forward(self, x):
        self.original_shape = x.shape

        return np_sum_to(x.data, self.target_shape)

    def backward(self, gy):
        return np.broadcast_to(gy, self.original_shape)


def sum_to(x, shape):
    if x.shape == shape:
        return as_variable(x)
    else:
        return SumTo(shape)(x)
