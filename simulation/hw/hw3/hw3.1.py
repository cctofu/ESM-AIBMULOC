import random
import seaborn as sns
import matplotlib.pyplot as plt
import math

def X(u):
    return math.pow(1-u, -1/3)

# Generate 100 samples
samples = [X(random.uniform(0, 1)) for _ in range(100)]

# Plot histogram with seaborn
sns.histplot(samples, bins=15, kde=True, color="skyblue", edgecolor="black")

plt.title("Pareto(α=3, xm=1) - 100 samples")
plt.xlabel("Value")
plt.ylabel("Frequency")

# Save to PNG
plt.savefig("pareto_100_runs_seaborn.png", dpi=300, bbox_inches="tight")
plt.show()