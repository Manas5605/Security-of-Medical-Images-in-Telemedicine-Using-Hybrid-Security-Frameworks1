import numpy as np

def logistic_map(size, x0=0.5, r=3.99):
    x = np.zeros(size)
    x[0] = x0
    for i in range(1, size):
        x[i] = r * x[i-1] * (1 - x[i-1])
    return (x * 256).astype(np.uint8)

def henon_map(size, a=1.4, b=0.3, x0=0.1, y0=0.3):
    x, y = np.zeros(size), np.zeros(size)
    x[0], y[0] = x0, y0
    for i in range(1, size):
        x[i] = 1 - a * x[i-1]**2 + y[i-1]
        y[i] = b * x[i-1]
    return (x * 256).astype(np.uint8)

def lorenz_system(size, dt=0.01, sigma=10, beta=8/3, rho=28, x0=0.1, y0=0.1, z0=0.1):
    x, y, z = np.zeros(size), np.zeros(size), np.zeros(size)
    x[0], y[0], z[0] = x0, y0, z0
    for i in range(1, size):
        dx = sigma * (y[i-1] - x[i-1])
        dy = x[i-1] * (rho - z[i-1]) - y[i-1]
        dz = x[i-1] * y[i-1] - beta * z[i-1]
        x[i] = x[i-1] + dt * dx
        y[i] = y[i-1] + dt * dy
        z[i] = z[i-1] + dt * dz
    return (x * 256).astype(np.uint8)

def generate_keys(shape):
    size = shape[0] * shape[1]
    
    logistic_keys = logistic_map(size).reshape(shape)
    henon_keys = henon_map(size).reshape(shape)
    lorenz_keys = lorenz_system(size).reshape(shape)

    return logistic_keys, henon_keys, lorenz_keys
