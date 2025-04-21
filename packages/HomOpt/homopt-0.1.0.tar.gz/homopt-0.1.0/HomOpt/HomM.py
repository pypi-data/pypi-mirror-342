import torch
from torch.optim import Optimizer

class HomM(Optimizer):
    def __init__(self, params, lr=0.1, a=-0.5, k1=-1.0, k2=-1.0, eps=0.2):
        """
        Finite-Time Momentum Optimizer

        Args:
            params (iterable): model parameters
            lr (float): learning rate
            a (float): exponent on the norm (usually negative)
            k1, k2 (float): gradient scaling coefficients
            eps (float): velocity coupling factor
        """
        defaults = dict(lr=lr, a=a, k1=k1, k2=k2, eps=eps)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        """
        Perform a single optimization step.
        """
        loss = closure() if closure is not None else None
        epsilon_min = 1e-5  # to avoid instability when norm is close to zero

        for group in self.param_groups:
            lr = group['lr']
            a = group['a']
            k1 = group['k1']
            k2 = group['k2']
            eps = group['eps']

            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad.data  # gradient tensor

                # Get state dict for this parameter
                state = self.state[p]

                # Initialize velocity buffer if not present
                if 'v' not in state:
                    state['v'] = torch.zeros_like(p.data)

                v = state['v']

                # Compute Euclidean norm: || [grad, v] ||
                norm_grad = torch.norm(grad)
                norm_v = torch.norm(v)
                norm_z = torch.sqrt(norm_grad ** 2 + norm_v ** 2)
                norm_z = torch.clamp(norm_z, min=epsilon_min)

                # Compute time-varying gain
                alpha = lr * norm_z.pow(a)

                # Explicit update (in-place)
                v.add_(alpha * (eps * grad + k2 * v))  # Update v
                p.data.add_(alpha * (k1 * grad + eps * v))  # Update p

        return loss
