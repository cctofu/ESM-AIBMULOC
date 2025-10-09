import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_X(n, rng=None):
    if rng is None:
        rng = np.random.default_rng()

    U = rng.uniform(0, 1, size=n)
    X = np.exp(1 - 1 / U)
    return X

if __name__ == "__main__":
    n = 100
    rng = np.random.default_rng(42)

    X = generate_X(n, rng)
    plt.figure(figsize=(7, 5))
    sns.histplot(X, bins=15, kde=True, color="mediumseagreen", edgecolor=None)
    plt.title("Distribution of X (Inverse Transform Sampling)")
    plt.xlabel("X")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("distribution_X_problem5.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ Saved figure as 'distribution_X_problem5.png'")
