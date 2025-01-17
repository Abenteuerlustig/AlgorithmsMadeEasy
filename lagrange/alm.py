"""
solve the following problem with Augmented Lagrange Multiplier method
min f(x) = -3x[0] - 5x[1]
s.t. x[0] + x[2] = 4
    2x[1] + x[3] = 12
    3x[0] + 2x[1] + x[4] = 18
    x[0], x[1], x[2], x[3], x[4] >= 0
"""

import torch


def lagrangian_function(x, lambda_):
    return f(x) + lambda_ @ (A @ x - b) + alpha / 2 * ((A @ x - b) ** 2).sum()


def f(x):
    return c @ x


def update_x(x, lambda_):
    """ update x with gradient descent """
    lagrangian_function(x, lambda_).backward()
    new_x = x - eta * x.grad
    x.data = new_x.clamp(min=0)  # ensure x not lower than zero
    x.grad.zero_()


def update_lambda(lambda_):
    lambda_.data = lambda_ + alpha * (A @ x - b)


def pprint(i, x, lambda_, epoch):
    print(f'\n{i}/{epoch}, L:{lagrangian_function(x, lambda_):.2f}, f(x): {f(x):.2f}')
    print(f'x: {x}')
    print(f'lambda: {lambda_}')
    print("constraints violation: " + str(A @ x - b))


def solve(x, lambda_):
    epoch = 500
    for i in range(epoch):
        pprint(i + 1, x, lambda_, epoch)
        update_x(x, lambda_)
        update_lambda(lambda_)


if __name__ == '__main__':
    eta = 0.03
    alpha = 1
    """
    min f(x) = c^T x
    s.t. Ax = b
    x >= 0
    """
    c = torch.tensor([-3, -5, 0, 0, 0], dtype=torch.float32)
    A = torch.tensor([[1, 0, 1, 0, 0], [0, 2, 0, 1, 0], [3, 2, 0, 0, 1]],
                     dtype=torch.float32)
    b = torch.tensor([4, 12, 18], dtype=torch.float32)

    lambda_ = torch.tensor([0, 0, 0], dtype=torch.float32)  # set the same dimension as b for lambda_
    x = torch.tensor([2, 0, 0, 0, 0], dtype=torch.float32, requires_grad=True)  # set random original value for iterating

    solve(x, lambda_)
