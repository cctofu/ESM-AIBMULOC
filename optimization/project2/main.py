import pandas as pd
from collections import defaultdict
from gurobipy import Model, GRB, quicksum

# ------------------------------
# 1. Load dataset and compute stats
# ------------------------------
df = pd.read_csv("games.csv")

# All teams and dates
teams = set(df["Home"]).union(set(df["Visitor"]))
dates = sorted(df["Date"].unique())

# Data structures
home_dates = defaultdict(list)       # (a)
home_vs_count = defaultdict(lambda: defaultdict(int))  # (b)
away_vs_count = defaultdict(lambda: defaultdict(int))  # (c)
away_dates = defaultdict(list)       # (d)

# Process each match (the code you already have)
for _, row in df.iterrows():
    date = row["Date"]
    home = row["Home"]
    away = row["Visitor"]

    # (a) Dates when team i played home
    home_dates[home].append(date)

    # (b) i played j at home
    home_vs_count[home][away] += 1

    # (c) i played j away = j played home
    away_vs_count[away][home] += 1

    # (d) Dates when team j played away
    away_dates[away].append(date)

# Convert lists to sets for quick membership tests
home_dates_set = {t: set(dlist) for t, dlist in home_dates.items()}
away_dates_set = {t: set(dlist) for t, dlist in away_dates.items()}

# ------------------------------
# 2. Build Gurobi model
# ------------------------------
m = Model("schedule_feasibility")

# Decision variables:
# x[d, i, j] = 1 if on date d team i plays at home vs team j
x = {}
for d in dates:
    for i in teams:
        for j in teams:
            if i == j:
                continue  # a team cannot play itself
            x[d, i, j] = m.addVar(vtype=GRB.BINARY, name=f"x_{d}_{i}_{j}")

m.update()

# ------------------------------
# 3. Constraints
# ------------------------------

# (e) For each team i, i plays home exactly on the dates computed in (a)
# i.e., for each date d:
#   if d in home_dates[i]: sum_j x[d, i, j] = 1
#   else:                  sum_j x[d, i, j] = 0
for i in teams:
    home_d = home_dates_set.get(i, set())
    for d in dates:
        expr = quicksum(x[d, i, j] for j in teams if j != i)
        if d in home_d:
            m.addConstr(expr == 1, name=f"home_date_{i}_{d}")
        else:
            m.addConstr(expr == 0, name=f"no_home_{i}_{d}")

# (f) For each team i, i plays away exactly on the dates computed in (d)
# i.e., for each date d:
#   if d in away_dates[i]: sum_j x[d, j, i] = 1
#   else:                  sum_j x[d, j, i] = 0
for i in teams:
    away_d = away_dates_set.get(i, set())
    for d in dates:
        expr = quicksum(x[d, j, i] for j in teams if j != i)
        if d in away_d:
            m.addConstr(expr == 1, name=f"away_date_{i}_{d}")
        else:
            m.addConstr(expr == 0, name=f"no_away_{i}_{d}")

# (Optional but natural) A team cannot play both home and away on the same date:
# sum_j x[d, i, j] + sum_j x[d, j, i] <= 1
# This is actually implied by (e) and (f) if your input is consistent, but it's nice to include.
for i in teams:
    for d in dates:
        expr = quicksum(x[d, i, j] for j in teams if j != i) + \
               quicksum(x[d, j, i] for j in teams if j != i)
        m.addConstr(expr <= 1, name=f"one_game_per_day_{i}_{d}")

# (g) For each ordered pair (i, j), i plays home vs j exactly
#     the number of times computed in (b)
for i in teams:
    for j in teams:
        if i == j:
            continue
        count_home_ij = home_vs_count[i][j]  # default 0 if not present
        expr = quicksum(x[d, i, j] for d in dates)
        m.addConstr(expr == count_home_ij, name=f"home_vs_{i}_{j}")

# (h) For each ordered pair (i, j), i plays away vs j exactly
#     the number of times computed in (c)
# Note: away_vs_count[i][j] = times i was away at j's home,
#       which is sum_d x[d, j, i].
for i in teams:
    for j in teams:
        if i == j:
            continue
        count_away_ij = away_vs_count[i][j]  # default 0 if not present
        expr = quicksum(x[d, j, i] for d in dates)
        m.addConstr(expr == count_away_ij, name=f"away_vs_{i}_{j}")

# ------------------------------
# 4. Dummy objective (feasibility only)
# ------------------------------
m.setObjective(0, GRB.MINIMIZE)

# Solve
m.optimize()

# ------------------------------
# 5. Extract one feasible schedule (if exists)
# ------------------------------
if m.status == GRB.OPTIMAL or m.status == GRB.SUBOPTIMAL:
    print("\nFeasible schedule found:\n")
    for d in dates:
        print(f"Date: {d}")
        for i in teams:
            for j in teams:
                if i == j:
                    continue
                if x[d, i, j].X > 0.5:
                    print(f"  {i} (home) vs {j} (away)")
        print()
else:
    print("No feasible schedule exists with the given constraints.")
