import matplotlib.pyplot as plt

# Data from the table
years = list(range(1996, 2007))   # 1996–2006
accidents = [
    3, 3, 1, 2, 2, 6, 0, 2, 1, 3, 2  # accidents from 1996–2006
]

# Plot bar chart
x = range(len(years))

plt.figure(figsize=(10, 6))
plt.bar(x, accidents, width=0.6, color="skyblue", edgecolor="black", label="Accidents")

plt.xticks(x, years, rotation=45)
plt.xlabel("Year")
plt.ylabel("Accidents")
plt.title("U.S. Airline Safety (1996–2006)")
plt.legend()
plt.tight_layout()
plt.show()
