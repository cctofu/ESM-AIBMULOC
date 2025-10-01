import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def sample_accept_reject(n=1):
    samples = []
    while len(samples) < n:
        Y = np.random.rand()        # proposal Y ~ Unif(0,1)
        U = np.random.rand()        # U ~ Unif(0,1)
        if U <= np.exp(Y - 1):      # acceptance condition
            samples.append(Y)
    return np.array(samples)

def inverse_method(u):
    return np.log(u*(np.e-1) + 1)

# Generate samples
samples_inverse = [inverse_method(random.uniform(0, 1)) for _ in range(100)]
samples_accept_reject = sample_accept_reject(100)

# Create two subplots side by side
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot inverse transform
sns.histplot(samples_inverse, bins=15, kde=True, color="skyblue", edgecolor="black", ax=axes[0])
axes[0].set_title("Inverse Transform Method - 100 samples")
axes[0].set_xlabel("Value")
axes[0].set_ylabel("Frequency")

# Plot acceptance–rejection
sns.histplot(samples_accept_reject, bins=15, kde=True, color="salmon", edgecolor="black", ax=axes[1])
axes[1].set_title("Acceptance–Rejection Method - 100 samples")
axes[1].set_xlabel("Value")
axes[1].set_ylabel("Frequency")

# Adjust layout and save
plt.tight_layout()
plt.savefig("comparison_inverse_vs_accept_reject.png", dpi=300, bbox_inches="tight")
plt.show()
