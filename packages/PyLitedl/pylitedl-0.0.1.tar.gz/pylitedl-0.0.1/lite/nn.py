# nn.py

# minitorch/nn.py
import numpy as np
from .tensor import Tensor

class Module:
    def parameters(self):
        return []

    def zero_grad(self):
        for p in self.parameters():
            p.grad = None

class Linear(Module):
    def __init__(self, in_features, out_features):
        self.weight = Tensor(np.random.randn(in_features, out_features) * np.sqrt(2. / in_features), requires_grad=True)
        self.bias = Tensor(np.zeros(out_features), requires_grad=True)

    def __call__(self, x: Tensor):
        out = Tensor(x.data @ self.weight.data + self.bias.data, requires_grad=True, _children=(x, self.weight, self.bias), _op='linear')

        def _backward():
            if x.requires_grad:
                x.grad = x.grad + (out.grad @ self.weight.data.T) if x.grad is not None else (out.grad @ self.weight.data.T)
            if self.weight.requires_grad:
                grad_w = x.data.T @ out.grad
                self.weight.grad = self.weight.grad + grad_w if self.weight.grad is not None else grad_w
            if self.bias.requires_grad:
                grad_b = np.sum(out.grad, axis=0)
                self.bias.grad = self.bias.grad + grad_b if self.bias.grad is not None else grad_b

        out._backward = _backward
        return out

    def parameters(self):
        return [self.weight, self.bias]
