import numpy as np
from .tensor import Tensor


class RNNCell:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        self.input_size = input_size

        # Initialize weights for input-to-hidden, hidden-to-hidden, and bias
        self.W_xh = Tensor(np.random.randn(input_size, hidden_size) * np.sqrt(2. / input_size), requires_grad=True)
        self.W_hh = Tensor(np.random.randn(hidden_size, hidden_size) * np.sqrt(2. / hidden_size), requires_grad=True)
        self.b_h = Tensor(np.zeros(hidden_size), requires_grad=True)

    def forward(self, x, h_prev):
        h = np.tanh(np.dot(x, self.W_xh.data) + np.dot(h_prev, self.W_hh.data) + self.b_h.data)
        return h

    def parameters(self):
        return [self.W_xh, self.W_hh, self.b_h]


class RNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.rnn_cell = RNNCell(input_size, hidden_size)
        self.W_hy = Tensor(np.random.randn(hidden_size, output_size) * np.sqrt(2. / hidden_size), requires_grad=True)
        self.b_y = Tensor(np.zeros(output_size), requires_grad=True)

    def forward(self, X):
        batch_size, seq_len, _ = X.data.shape
        h = np.zeros((batch_size, self.rnn_cell.hidden_size))

        for t in range(seq_len):
            h = self.rnn_cell.forward(X.data[:, t, :], h)

        y = np.dot(h, self.W_hy.data) + self.b_y.data
        return Tensor(y, requires_grad=True, _children=(X,), _op='rnn')

    def parameters(self):
        return self.rnn_cell.parameters() + [self.W_hy, self.b_y]
