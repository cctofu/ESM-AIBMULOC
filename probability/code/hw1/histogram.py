import matplotlib.pyplot as plt

# Fatalities data from 1996–2006 (last 11 entries)
fatalities = [
    342, 3, 1, 12, 89, 531, 0, 22, 13, 22, 50
]

# Plot histogram with bin size 50
plt.figure(figsize=(10, 6))
plt.hist(fatalities, bins=range(0, max(fatalities) + 50, 50), 
         edgecolor="black", color="skyblue")

plt.xlabel("Fatalities (binned, size=50)")
plt.ylabel("Frequency (years)")
plt.title("Histogram of Yearly Fatalities (1996–2006)")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
