# OPTIMIZATION ASSIGNMENT 1

Calvin Chang 09/21/2025 **calculations done using gurobi in python*

> ## Problem #1

#### <u>Decision Variables:</u>
Based on the question, there are 3 different variables that needs to be used when finding the maximum profit, the **amount of crude oil** purchased, the **amount of aviation fuel** sent to cracker, and the **amount of heating oil** sent to crackers, which gives the 3 variables:
$$
x \geq 0 \\
a \geq 0\\
h \geq 0
$$

#### <u>Objective function:</u>

The objective is to maximum for Sunco's daily profit, the profit can also be known as the formula $\text{Profit} = \text{Revenue} - \text{Cost}$. Based on this formula, we can find the variables. The cost for crude oil we know is: 
$$
-40x
$$
Revenue for distilled oil:
$$
0.5x*60 + 0.5x*40 = 50x
$$
Revenue for cracker:
$$
70a + 50h
$$


Therefore, Objective function is to **maximize** for: 
$$
50x + 70a + 50h - 40x\\
= 10x + 70a + 50h
$$

#### <u>Constraints:</u>

Since all aviation fuel and heating oil must come from crude oil we know:
$$
a \leq 0.5x \\
h \leq 0.5x \\
$$

And the cracker time limitations and max crude oil barrel purchases give:
$$
a + 0.75h \leq 8 \\
x \leq 20
$$

#### <u>Optimal Solution found:</u>

```
760.0
crude_oil 20.0
aviation_oil 8.0
heating_oil 0.0
```

==Maximum profit: $\$760,000$==

--------

> ## Problem #2

#### <u>Decision Variables:</u>

Based on the problem statement, we define the decision variables as follows: the number of times **process 1** is executed, the number of times **process 2** is executed, and the number of promoter hours allocated:
$$
x1, x2 \geq 0\\
p \geq 0
$$

#### <u>Objective function:</u>

Objective is to **maximize** profit, which is equal to $\text{Profit} = \text{Revenue} - \text{Cost}$.

Revenue:
$$
5(3*x1+5*x2)
$$
Cost:
$$
3(x1+2*x2)+2(2*x1+3*x2) + 100*p\\
= 7*x1 + 12*x2 + 100*p
$$

Therefore, Objective function is **maximize** for:
$$
15*x1 + 25*x2 - (7*x1 + 12*x2 + 100*p)\\
= 8*x1 + 13*x2 - 100*p
$$

#### <u>Constraints:</u>

Based on constraints from max labor units, max chemical units, and demand, we can get constraint functios of:
$$
x1 + 2*x2 \leq 20,000\\
2*x1 + 3*x2 \leq 35,000\\
3*x1 + 5*x2 \leq 1000 + 200*p
$$

#### <u>Optimal Solution found:</u>

```
118000.0
process_1_runs 10000.0
process_2_runs 5000.0
promoter_hours 270.0
```

==Maximum profit: $\$118,000$==

--------

> ## Problem #3

#### <u>Decision Variables:</u>

Based on the question, we need the following variables:

crude oil processed by methods 1, 2, 3 correspondingly:
$$
x1, x2, x3 \geq 0
$$
oil cracked from 6 to 8 and 8 to 10:
$$
c1, c2 \geq 0
$$
grade 6, 8, 10 crude oil thats blended into gas:
$$
y1, y2, y3 \geq 0
$$
grade 6, 8, 10 crude oil thats blended into heating oil:
$$
z1, z2, z3 \geq 0
$$

#### <u>Objective function:</u>

The output of the process is the total gas and the total heating oil:
$$
(y1 + y2 + y3) + (z1 + z2 + z3)\\
G = y1 + y2 + y3 \\
H = z1 + z2 + z3
$$
The revenue of the output can be found by:
$$
12G + 5H
$$
The cost of the output can be found by:
$$
(3.4*x1 + 3.0*x2 + 2.6*x3) + (1*c1 + 1.5*c2)
$$
Therefore, the Objective function is to **maximize** for:
$$
12G + 5H - [(3.4*x1 + 3.0*x2 + 2.6*x3) + (1*c1 + 1.5*c2)]
$$
#### <u>Constraints:</u>
Based on Sales capacity:
$$
G \leq 2000 \\
H \leq 600 \\
$$
Average grade requirements:
$$
6*y1 + 8*y2 + 10*y3 \leq 9G\\
6*z1 + 8*z2 + 10*z3 \leq 7H
$$

Cracking balance based on different methods:
$$
y1 + z1 = (0.3*x1 + 0.4*x2 + 0.1*x3) - c1\\
y2 + z2 = (0.5*x1 + 0.2*x2 + 0.3*x3) + c1 - c2\\
y3 + z3 = (0.8*x1 + 0.4*x2 + 0.2*x3) + c2
$$

#### <u>Optimal Solution found:</u>

```
21475.0
crude_oil_method1 1625.0
crude_oil_method2 0.0
crude_oil_method3 0.0
cracked6_8 0.0
cracked8_10 0.0
grade6g 187.5
grade8g 512.5
grade10g 1300.0
grade6h 300.0
grade8h 300.0
grade10h 0.0
```

==Maximum profit: $\$21,475$==

--------

> ## Problem #4

#### <u>Decision Variables:</u>

Based on the problem, we have variables that correspond to the amount of stock sold from stock 1 to stock 10:
$$
x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 \geq 0
$$

#### <u>Objective function:</u>

We simply have to **maximize** for the value of the stocks left after selling the $x1, x2, ..., x10$ amount of stocks:
$$
\sum_{i=1}^{10} (100 - x_i) * \text{Future}_i
$$

#### <u>Constraints:</u>

We can define $c_i$ as the $\text{Current}_i$, and $p_i$ as the $\text{Purchase}_i$ for prices. The tax cost and transaction cost for each individual stock $i$ sold can then be found by:
$$
0.3 * x_i(c_i - p_i)\\
0.01 * x_i * c_i
$$
The total tax and total transaction cost is then:
$$
\sum_{i=1}^{10} 0.3 * x_i * (c_i - p_i)\\
\sum_{i=1}^{10} (0.01 * x_i * c_i)
$$

we have to ensure the amount we sell is equal to $\$300,000$, Therefore the constraints are:
$$
\sum_{i=1}^{10} [(x_i * c_i) - (0.3 * x_i * (c_i - p_i)) - (0.01 * x_i * c_i)] = 300,000
$$

#### <u>Optimal Solution found:</u>

```
20893.708807669263
sell_stock[0] 0.0
sell_stock[1] 0.0
sell_stock[2] 100.0
sell_stock[3] 100.0
sell_stock[4] 0.0
sell_stock[5] 63.75074895146793
sell_stock[6] 0.0
sell_stock[7] 100.0
sell_stock[8] 100.0
sell_stock[9] 100.0
```

==Maximum future profit: $\$20893.709$==

--------

> ## Problem #5

#### <u>Decision Variables:</u>

Based on the given problem, the decision variables is the amount borrowed from $n$ credit lines for each month:
$$
\begin{bmatrix}
x_{1,1} & x_{1,2} & \cdots & x_{1,n} \\
x_{2,1} & x_{2,2} & \cdots & x_{2,n} \\
\vdots  & \vdots  & \ddots & \vdots  \\
x_{T,1} & x_{T,2} & \cdots & x_{T,n} \\
\end{bmatrix}
$$

#### <u>Objective function:</u>
The $\text{excess}_i$ for each month $t$ can then be respresented as:
$$
\text{payment due from 1 month ago}: R_{-1} = r_{-1}^{1} + r_{-1}^{2} + ... r_{-1}^{n}\\
\text{payment due from 2 month ago}: R_{-2} = r_{-2}^{1} + r_{-2}^{2} + ... r_{-2}^{n}\\
\text{payment due from 3 month ago}: R_{-3} = r_{-3}^{1} + r_{-3}^{2} + ... r_{-3}^{n}\\
(1+r)*c_{t-1}+c_t + (x_{t,1} + x_{t,2} + ... + x_{t,n}) - R_{-1} - R_{-2} - R_{-3}
$$
Therefore, the objective function is to **maximize** the value of function:
$$
(1+r)*c_{T-1} + c_T - R_{-1} - R_{-2} - R_{-3}
$$
#### <u>Constraints:</u>
For the given matrix of size $n * T$, every value has a lower bound $\geq 0$, and the upper bound for each line $i$ cannot exceed its capacity $\beta_i$ if it’s still usable, or is set to zero once past the last usable month.
#### <u>Collab notebook usage</u>

I've implemented two different ways of running the function `maximize_excess_funds`, one is to enter each of the following variables manually and one is to modify the preset data dictionary to enter the values:

```
T						# number of months
n						# number of credit lines
c						# array of cash flows for T months
r						# interest rate for excess funds
beta				# Max borrow amount for each credit line
r1					# array of each r1 for each credit line
r2					# array of each r2 for each credit line
r3					# array of each r3 for each credit line
```

The function can then be called to solve the function and will output the maximum excess funds amount

--------

> ## AI usage

The coding, writeup and calculations for `Problem1`,  `Problem2`, `Problem3`, `Problem4` were all done individually. However, while attempting `Problem 5` I was able to formulate my own functions, but had trouble formulating these functions into gurobi constraints, so I utilized GPT mainly to learn how to dynamically calculate and add constraints that were not as simple as the previous problems. Most of the code was still handwritten, the parts that used the help of **Chatgpt** are:

```python
# Last usable month for each line so all repayments finish by T
last_use = []
for i in lines:
    max_lag = 0
    if r1[i] > 0: max_lag = max(max_lag, 1)
    if r2[i] > 0: max_lag = max(max_lag, 2)
    if r3[i] > 0: max_lag = max(max_lag, 3)
    last_use.append(T - max_lag if max_lag > 0 else T)

# Per-month borrowing caps
for i in lines:
    for t in months:
        borrow[i, t].UB = beta[i] if t <= last_use[i] else 0
```

