import numpy as np

def g(u):
    return np.exp(u + u**2)

def monte_carlo_simulation(n):
    u_arr = []
    for _ in range(n):
        u = np.random.uniform(0,1)
        v = -2 + 4*u
        u_arr.append(v)
    x = (4/n) * sum([g(u) for u in u_arr])
    return x

if __name__ == "__main__":
    N = 1000
    res = monte_carlo_simulation(N)
    print(res)