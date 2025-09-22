import random
import seaborn as sns
import matplotlib.pyplot as plt

def roll_dice():
    seen = set()
    rolls = 0														
    while len(seen) < 6:
        dice_roll = random.randint(1, 6)	
        seen.add(dice_roll)
        rolls += 1
    return rolls

if __name__ == "__main__":
    samples = [roll_dice() for _ in range(100)]

    plt.figure(figsize=(8,5))
    sns.histplot(samples, bins=range(min(samples), max(samples)+2), discrete=True, stat="count", color="steelblue", edgecolor="black")
    plt.xlabel("Total rolls until all 6 faces seen")
    plt.ylabel("Count")
    plt.title("Dice distribution")
    plt.savefig("./graphs/die_roll_100.png", dpi=300)