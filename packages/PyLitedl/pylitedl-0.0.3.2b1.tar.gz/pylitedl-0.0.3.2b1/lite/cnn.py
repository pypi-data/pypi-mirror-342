import numpy as np
from .tensor import Tensor


class Conv2D:
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

        # Initialize filters (weights) and biases
        self.weights = Tensor(
            np.random.randn(out_channels, in_channels, kernel_size, kernel_size) * np.sqrt(2. / in_channels),
            requires_grad=True)
        self.bias = Tensor(np.zeros(out_channels), requires_grad=True)

    def __call__(self, x: Tensor):
        # Apply convolution (simple valid padding)
        batch_size, in_channels, in_height, in_width = x.data.shape
        kernel_size = self.kernel_size
        stride = self.stride
        padding = self.padding

        # Pad input if necessary
        if padding > 0:
            x.data = np.pad(x.data, ((0,), (0,), (padding,), (padding,)), mode='constant', constant_values=0)

        out_height = (x.data.shape[2] - kernel_size) // stride + 1
        out_width = (x.data.shape[3] - kernel_size) // stride + 1

        out = np.zeros((batch_size, self.out_channels, out_height, out_width))

        for i in range(out_height):
            for j in range(out_width):
                # Slice the input for the convolution operation
                x_slice = x.data[:, :, i * stride:i * stride + kernel_size, j * stride:j * stride + kernel_size]
                out[:, :, i, j] = np.tensordot(x_slice, self.weights.data, axes=((1, 2, 3), (1, 2, 3))) + self.bias.data

        out = Tensor(out, requires_grad=True, _children=(x,), _op='conv2d')
        return out

    def parameters(self):
        return [self.weights, self.bias]


class MaxPool2D:
    def __init__(self, pool_size, stride):
        self.pool_size = pool_size
        self.stride = stride

    def __call__(self, x: Tensor):
        batch_size, in_channels, in_height, in_width = x.data.shape
        pool_size = self.pool_size
        stride = self.stride

        out_height = (in_height - pool_size) // stride + 1
        out_width = (in_width - pool_size) // stride + 1

        out = np.zeros((batch_size, in_channels, out_height, out_width))

        for i in range(out_height):
            for j in range(out_width):
                x_slice = x.data[:, :, i * stride:i * stride + pool_size, j * stride:j * stride + pool_size]
                out[:, :, i, j] = np.max(x_slice, axis=(2, 3))

        out = Tensor(out, requires_grad=True, _children=(x,), _op='maxpool')
        return out
