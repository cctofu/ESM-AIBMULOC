import numpy as np

def g(u):
    return u**2 + (1-u)**2

def monte_carlo_simulation(n):
    sum = 0
    for _ in range(n):
        U = np.random.uniform(0,1)
        denom = g(U)
        val = (U*(1-U)) / (denom**2)
        sum += val
    x = (1/n) * sum
    return x

if __name__ == "__main__":
    N = 1000
    res = monte_carlo_simulation(N)
    print(res)