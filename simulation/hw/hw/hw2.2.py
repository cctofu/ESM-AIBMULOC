import random
import seaborn as sns
import matplotlib.pyplot as plt
import math
import pandas as pd

# ----- part (b) implementation START ------
def NB_b(r,p):
    U = random.uniform(0,1) 					
    k = r										
    pmf = p**r						  
    cdf = pmf								

    while U > cdf:
        pmf = pmf * (k*(1-p)/(k-r+1)) 
        k += 1
        cdf += pmf
    return k
# ----- part (b) implementation END ------

# ----- part (c) implementation START ------
def geom(p):
    U = random.uniform(0,1) 	   																
    result = 1 + math.floor(math.log(1 - U) / math.log(1 - p))			
    return result

def NB_c(r, p):
    k = 0
    for i in range(r):
        G = geom(p)
        k += G
    return k
# ----- part (c) implementation END ------

# ----- part (d) implementation START ------
def NB_d(r, p):
    success = 0
    trials = 0
    while success < r:
        U = random.uniform(0,1) 
        if U < p:      
            success += 1
        trials += 1
    return trials
# ----- part (d) implementation END ------

if __name__ == "__main__":
    r, p = 2, 1/3

    samples_b = [NB_b(r, p) for _ in range(100)]
    samples_c = [NB_c(r, p) for _ in range(100)]
    samples_d = [NB_d(r, p) for _ in range(100)]

    # Plot
    plt.figure(figsize=(12, 6))

    sns.histplot(samples_b, color="red", label="Part (b)", stat="probability", discrete=True, binwidth=1)
    sns.histplot(samples_c, color="blue", label="Part (c)", stat="probability", discrete=True, binwidth=1)
    sns.histplot(samples_d, color="green", label="Part (d)", stat="probability", discrete=True, binwidth=1)

    plt.xlabel("k")
    plt.ylabel("Probability")
    plt.title("NB(2, 1/3) distribution overlay")
    plt.legend()
    plt.savefig("./graphs/NB_distribution_over.png", dpi=300)

    df = pd.DataFrame({
        "Part (b)": samples_b,
        "Part (c)": samples_c,
        "Part (d)": samples_d
    }).melt(var_name="Method", value_name="k")

    plt.figure(figsize=(12,6))
    sns.histplot(df, x="k", hue="Method", stat="probability", discrete=True,
                multiple="dodge", shrink=0.8)
    plt.title("NB(2, 1/3) distribution side by side")
    plt.savefig("./graphs/NB_distribution_side.png", dpi=300)