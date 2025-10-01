import random
import math
import seaborn as sns
import matplotlib.pyplot as plt

def geom(p):
    U = random.uniform(0,1)
    return 1 + math.floor(math.log(1 - U) / math.log(1 - p))

def X():
    flip = random.uniform(0,1) 						
    if flip < 0.5:
        return geom(1/2)   
    else:
        return geom(1/3)  

if __name__ == "__main__":
    samples = [X() for _ in range(100)]

    plt.figure(figsize=(8, 5))
    sns.histplot(samples, stat="probability", discrete=True, binwidth=1, color="blue", edgecolor="black")

    plt.xlabel("j")
    plt.ylabel("Relative frequency")
    plt.title("Distribution of X")
    plt.savefig("./graphs/X_distribution.png", dpi=300)  # save to file