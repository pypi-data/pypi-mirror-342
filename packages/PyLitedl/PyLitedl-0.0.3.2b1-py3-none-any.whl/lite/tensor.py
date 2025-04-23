import numpy as np
import pickle
import os

class Tensor:
    def __init__(self, data, requires_grad=False, _children=(), _op=''):
        self.data = np.array(data, dtype=np.float32)
        self.requires_grad = requires_grad
        self.grad = None

        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __repr__(self):
        return f"Tensor({self.data}, requires_grad={self.requires_grad}, grad={self.grad})"

    def item(self):
        return self.data.item()

    def numpy(self):
        return self.data

    def backward(self, grad=None):
        if not self.requires_grad:
            return

        if grad is None:
            if self.data.size != 1:
                raise RuntimeError("grad must be specified for non-scalar outputs.")
            grad = np.ones_like(self.data)

        self.grad = grad
        visited = set()
        topo_order = []

        def build_topo(tensor):
            if tensor not in visited:
                visited.add(tensor)
                for child in tensor._prev:
                    build_topo(child)
                topo_order.append(tensor)

        build_topo(self)

        for tensor in reversed(topo_order):
            tensor._backward()

    # Basic Ops
    def __add__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data + other.data, requires_grad=self.requires_grad or other.requires_grad, _children=(self, other), _op='+')

        def _backward():
            if self.requires_grad:
                self.grad = self.grad + out.grad if self.grad is not None else out.grad
            if other.requires_grad:
                other.grad = other.grad + out.grad if other.grad is not None else out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data * other.data, requires_grad=self.requires_grad or other.requires_grad, _children=(self, other), _op='*')

        def _backward():
            if self.requires_grad:
                grad = other.data * out.grad
                self.grad = self.grad + grad if self.grad is not None else grad
            if other.requires_grad:
                grad = self.data * out.grad
                other.grad = other.grad + grad if other.grad is not None else grad
        out._backward = _backward
        return out

    def __neg__(self): return self * -1
    def __sub__(self, other): return self + (-other)
    def __truediv__(self, other): return self * other**-1

    def __pow__(self, power):
        assert isinstance(power, (int, float)), "only int/float powers supported"
        out = Tensor(self.data ** power, requires_grad=self.requires_grad, _children=(self,), _op=f'**{power}')

        def _backward():
            if self.requires_grad:
                grad = (power * self.data ** (power - 1)) * out.grad
                self.grad = self.grad + grad if self.grad is not None else grad
        out._backward = _backward
        return out

    # Saving & Loading
    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump({
                'data': self.data,
                'grad': self.grad,
                'requires_grad': self.requires_grad
            }, f)

    @staticmethod
    def load(filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No such file: {filepath}")
        with open(filepath, 'rb') as f:
            obj = pickle.load(f)
        t = Tensor(obj['data'], requires_grad=obj['requires_grad'])
        t.grad = obj['grad']
        return t


# Helper like torch.tensor()
def tensor(data, requires_grad=False):
    return Tensor(data, requires_grad=requires_grad)

