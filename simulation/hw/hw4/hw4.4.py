import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_X(n, rng=None):
    if rng is None:
        rng = np.random.default_rng()

    # Step 1: mixture component
    B = rng.choice([0, 1], size=n, p=[0.5, 0.5])

    # Step 2: sample X from the corresponding geometric distribution
    X = np.empty(n, dtype=int)
    U = rng.uniform(0, 1, size=n)

    # Case 1: B = 0 → Geometric(p=1/2)
    mask0 = (B == 0)
    X[mask0] = np.floor(np.log(1 - U[mask0]) / np.log(1 - 0.5)).astype(int) + 1

    # Case 2: B = 1 → Geometric(p=1/3)
    mask1 = (B == 1)
    X[mask1] = np.floor(np.log(1 - U[mask1]) / np.log(1 - 1/3)).astype(int) + 1

    return X
    

if __name__ == "__main__":
    n = 100
    rng = np.random.default_rng(42)
    X = generate_X(n, rng)
    plt.figure(figsize=(7, 5))
    sns.countplot(x=X, color="steelblue")
    plt.title("Distribution of X (Composition Method)")
    plt.xlabel("X")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("composition_X_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved figure as 'composition_X_distribution.png'")
