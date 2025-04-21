# minitorch/losses.py
import numpy as np
from .tensor import Tensor


def mse_loss(pred: Tensor, target: Tensor) -> Tensor:
    """
    Mean Squared Error Loss: (1/n) * Σ(pred - target)^2
    """
    diff = pred - target
    loss_value = (diff * diff).mean()  # average over all examples

    # Return the loss as a tensor that can be used in backward pass
    out = Tensor(loss_value, requires_grad=True)

    def _backward():
        # The gradient of MSE w.r.t. prediction is:
        # grad = 2 * (pred - target) / n
        if pred.requires_grad:
            grad = 2 * (pred.data - target.data) / pred.data.shape[0]
            pred.grad = grad if pred.grad is None else pred.grad + grad

    out._backward = _backward
    return out


def cross_entropy_loss(logits: Tensor, target: np.ndarray) -> Tensor:
    """
    Cross Entropy Loss: -Σ(target * log(probs))
    """
    logits_data = logits.data
    shifted_logits = logits_data - np.max(logits_data, axis=1, keepdims=True)  # for numerical stability
    exp_scores = np.exp(shifted_logits)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

    # Get the number of samples (N)
    N = logits_data.shape[0]

    # Cross-entropy loss value
    log_likelihood = -np.log(probs[range(N), target])
    loss_value = np.sum(log_likelihood) / N

    out = Tensor(loss_value, requires_grad=True)

    def _backward():
        # The gradient of the loss w.r.t. logits (logits gradients)
        grad = probs
        grad[range(N), target] -= 1  # subtract target class prob
        grad = grad / N
        logits.grad = grad if logits.grad is None else logits.grad + grad

    out._backward = _backward
    return out
