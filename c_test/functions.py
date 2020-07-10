import numpy as np


def orbital_mechanics(t, x, mu):
    r = np.linalg.norm(x[0:3])

    mu_r3 = mu/r**3
    a = np.array([[0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 1],
                  [-mu_r3, 0, 0, 0, 0, 0],
                  [0, -mu_r3, 0, 0, 0, 0],
                  [0, 0, -mu_r3, 0, 0, 0]])

    return np.dot(a, x)


def rk4(t0, t1, dt, x0, y, **kwargs):
    t_range = np.arange(t0, t1 + dt, dt)
    state = np.empty((len(t_range), 6))
    state[0] = x0

    for i, t in enumerate(t_range[:-1]):
        cs = state[i]

        k1 = dt * y(t, cs, **kwargs)
        k2 = dt * y(t + 0.5*dt, cs + 0.5*k1, **kwargs)
        k3 = dt * y(t + 0.5*dt, cs + 0.5*k2, **kwargs)
        k4 = dt * y(t + dt, cs + k3, **kwargs)

        state[i + 1] = state[i] + 1/6*k1 + 1/3*k2 + 1/3*k3 + 1/6*k4

    return state


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    mu = 3.98600441e5
    
    x = rk4(0, 7200, 1, np.array([8000, 0, 0, 0, np.sqrt(mu/8000), 0]), orbital_mechanics, mu=mu)

    plt.plot(x[:, 0], x[:, 1])
    plt.show()
