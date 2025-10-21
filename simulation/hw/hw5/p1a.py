import numpy as np

def g(u):
    return np.exp(np.exp(u))

def monte_carlo_simulation(n):
    u_arr = []
    for _ in range(n):
        u = np.random.uniform(0,1)
        u_arr.append(g(u))
    x = (1/n) * sum(u_arr)
    return x

if __name__ == "__main__":
    N = 1000
    res = monte_carlo_simulation(N)
    print(res)