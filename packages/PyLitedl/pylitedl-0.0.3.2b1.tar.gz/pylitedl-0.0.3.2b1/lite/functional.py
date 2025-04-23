# minitorch/functional.py
import numpy as np
from .tensor import Tensor

def relu(x: Tensor) -> Tensor:
    out = Tensor(np.maximum(0, x.data), requires_grad=x.requires_grad, _children=(x,), _op='ReLU')

    def _backward():
        if x.requires_grad:
            grad = (x.data > 0).astype(np.float32) * out.grad
            x.grad = x.grad + grad if x.grad is not None else grad

    out._backward = _backward
    return out

def sigmoid(x: Tensor) -> Tensor:
    data = 1 / (1 + np.exp(-x.data))
    out = Tensor(data, requires_grad=x.requires_grad, _children=(x,), _op='sigmoid')

    def _backward():
        if x.requires_grad:
            grad = data * (1 - data) * out.grad
            x.grad = x.grad + grad if x.grad is not None else grad

    out._backward = _backward
    return out
