import matplotlib.pyplot as plt

# Data from the table (1996–2006 only)
years = list(range(1996, 2007))
accidents = [
    3, 3, 1, 2, 2, 6, 0, 2, 1, 3, 2  # accidents for 1996–2006
]

# Plot a time series line chart
plt.figure(figsize=(10, 6))
plt.plot(years, accidents, marker='o', linestyle='-', color='tab:red', label="Accidents")

plt.xticks(years, rotation=45)
plt.xlabel("Year")
plt.ylabel("Accidents")
plt.title("U.S. Airline Safety (1996–2006) - Accidents Over Time")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
