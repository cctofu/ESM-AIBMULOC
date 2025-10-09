import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def sample_rejection(n, M=10.0, rng=None):
    """Rejection sampling from region A."""
    if rng is None:
        rng = np.random.default_rng()

    xs, ys = [], []
    tries = 0
    while len(xs) < n:
        x = rng.uniform(-1.0, 1.0)
        y = rng.uniform(-M, M)
        tries += 1
        # Accept if inside region A
        if np.abs(y) <= min(M, (np.abs(x) ** -0.5 if x != 0 else np.inf)):
            xs.append(x)
            ys.append(y)
    accept_rate = n / tries
    print(f"[Rejection Sampling] acceptance rate = {accept_rate:.3f}")
    return np.array(xs), np.array(ys)


def sample_direct(n, rng=None):
    """Direct (conditional) sampling method."""
    if rng is None:
        rng = np.random.default_rng()

    sign = rng.choice([-1.0, 1.0], size=n)
    U = rng.uniform(0, 1, size=n)
    X = sign * (U ** 2)

    V = rng.uniform(0, 1, size=n)
    band = np.power(np.abs(X), -0.5, where=(np.abs(X) > 0))
    Y = (2 * V - 1) * band
    return X, Y


def plot_seaborn(X, Y, M, title, filename):
    """Plot samples using Seaborn and save as image."""
    sns.set(style="whitegrid", font_scale=1.2)
    plt.figure(figsize=(6, 5))
    sns.scatterplot(x=X, y=Y, s=50, color="royalblue", edgecolor=None)
    plt.xlim(-1.05, 1.05)
    plt.ylim(-M, M)
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved figure as '{filename}'")


if __name__ == "__main__":
    n = 100
    M = 10
    rng = np.random.default_rng(42)

    # --- Rejection Sampling ---
    Xr, Yr = sample_rejection(n, M, rng)
    plot_seaborn(Xr, Yr, M, "Uniform Samples in Region A (Rejection)", "region_A_rejection.png")

    # --- Direct Sampling ---
    Xd, Yd = sample_direct(n, rng)
    plot_seaborn(Xd, Yd, M, "Uniform Samples in Region A (Direct)", "region_A_direct.png")
