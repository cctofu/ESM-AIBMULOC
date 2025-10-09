import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ----- Parameters -----
M = 2 * np.pi * np.exp(0.5)   # envelope constant
N = 100                       # number of accepted samples

# ----- Unnormalized target function f*(x, y) -----
def f_star(x, y):
    return np.exp(-x**2 - y**2 + x * np.sin(x * y))

# ----- Proposal density g(x, y): standard normal -----
def g_pdf(x, y):
    return (1 / (2 * np.pi)) * np.exp(-0.5 * (x**2 + y**2))

# ----- Acceptance-Rejection Sampling -----
accepted = []
attempts = 0

while len(accepted) < N:
    # 1. Propose (X, Y) from N(0, 1)
    x, y = np.random.randn(), np.random.randn()
    
    # 2. Draw U ~ Uniform(0, 1)
    u = np.random.rand()
    
    # 3. Compute acceptance ratio
    ratio = f_star(x, y) / (M * g_pdf(x, y))
    
    # 4. Accept or reject
    if u <= ratio:
        accepted.append((x, y))
    
    attempts += 1

accepted = np.array(accepted)
X, Y = accepted[:, 0], accepted[:, 1]

print(f"Accepted {N} samples after {attempts} total draws (acceptance rate = {N/attempts:.3f})")

# ----- Plot distributions -----
sns.set(style="whitegrid", font_scale=1.2)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(X, kde=True, color="skyblue", ax=axes[0])
axes[0].set_title("Distribution of X")

sns.histplot(Y, kde=True, color="lightcoral", ax=axes[1])
axes[1].set_title("Distribution of Y")

plt.tight_layout()
output_file = "xy_distributions.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")
plt.close()
plt.show()
