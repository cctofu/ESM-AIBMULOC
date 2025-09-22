import random
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# Inverse transform method for Binomial(n, p)
def binom(n, p):
    if p == 0:
        return 0
    if p == 1:
        return n

    U = random.uniform(0, 1)
    k = 0
    pmf = (1 - p) ** n
    cdf = pmf

    while U > cdf and k < n:
        k += 1
        pmf = pmf * ((n - (k - 1)) / k) * (p / (1 - p))
        cdf += pmf

    return k

# Generate 100 samples
samples = [binom(10, 2/3) for _ in range(100)]
counts = Counter(samples)

# Prepare data for seaborn
x = list(counts.keys())
y = list(counts.values())

# Plot with seaborn
sns.barplot(x=x, y=y, color="skyblue", edgecolor="black")

plt.title("Distribution of 100 generations for Bin(10, 2/3)")
plt.xlabel("k")
plt.ylabel("Frequency")

# Save to PNG
plt.savefig("binom_100_runs_seaborn.png", dpi=300, bbox_inches="tight")
plt.show()
