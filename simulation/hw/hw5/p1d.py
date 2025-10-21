import numpy as np

def monte_carlo_simulation(n):
    h = []
    for _ in range(n):
        U = np.random.uniform(0, 1)
        X = -np.log(U)
        V = np.random.uniform(0, 1)
        Y = -np.log(V)
        if Y <= (X**2):
            h.append(np.sin(X*Y))
        else:
            h.append(0)
    return (1/n) * sum(h)

if __name__ == "__main__":
    N = 1000
    res = monte_carlo_simulation(N)
    print(res)