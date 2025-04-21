import numpy as np
from .tensor import Tensor
from .nn import Linear
class QNet:
    def __init__(self, input_size, output_size):
        self.fc1 = Linear(input_size, 128)
        self.fc2 = Linear(128, 64)
        self.fc3 = Linear(64, output_size)  # Q-values for each action

    def forward(self, state: Tensor):
        x = self.fc1(state)
        x = self.fc2(x)
        q_values = self.fc3(x)
        return q_values

    def parameters(self):
        return self.fc1.parameters() + self.fc2.parameters() + self.fc3.parameters()
