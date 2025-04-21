from scipy.optimize import minimize
import numpy as np

class SciPyOptimizer:
    def __init__(self, params, loss_fn, lr=1e-3, method='L-BFGS-B'):
        self.params = params  # Parameters to optimize (typically your model's weights)
        self.loss_fn = loss_fn  # Loss function
        self.lr = lr  # Learning rate (if used)
        self.method = method  # Optimization method (L-BFGS-B, BFGS, etc.)

    def objective(self, flat_params):
        self.unpack(flat_params)
        pred = model(X)  # Forward pass
        loss = self.loss_fn(pred, y)  # Calculate loss
        model.zero_grad()
        loss.backward()  # Backward pass
        grad_flat = np.concatenate([p.grad.flatten() for p in self.params])  # Flatten gradients
        return loss.item(), grad_flat

    def pack(self):
        return np.concatenate([p.data.flatten() for p in self.params])  # Flatten parameters

    def unpack(self, flat_params):
        i = 0
        for p, shape, size in zip(self.params, shapes, sizes):
            p.data = flat_params[i:i+size].reshape(shape)
            i += size

    def step(self):
        # Use scipy.optimize.minimize to optimize parameters
        result = minimize(fun=lambda w: self.objective(w),
                          x0=self.pack(),
                          method=self.method,
                          jac=True,
                          options={'maxiter': 100})
        self.unpack(result.x)
