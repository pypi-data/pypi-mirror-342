# minitorch/scipy_optim.py
import numpy as np
from scipy.optimize import minimize

def scipy_optimizer(model, loss_fn, X, y, method='L-BFGS-B', max_iter=100):

    params = model.parameters()
    shapes = [p.data.shape for p in params]
    sizes = [np.prod(s) for s in shapes]

    def pack():
        return np.concatenate([p.data.flatten() for p in params])

    def unpack(flat_params):
        i = 0
        for p, shape, size in zip(params, shapes, sizes):
            p.data = flat_params[i:i+size].reshape(shape)
            i += size

    def objective(flat_params):
        unpack(flat_params)
        pred = model(X)
        loss = loss_fn(pred, y)
        model.zero_grad()
        loss.backward()
        grad_flat = np.concatenate([p.grad.flatten() for p in params])
        return loss.item(), grad_flat

    result = minimize(fun=lambda w: objective(w),
                      x0=pack(),
                      method=method,
                      jac=True,
                      options={'maxiter': max_iter})

    unpack(result.x)
    return result
