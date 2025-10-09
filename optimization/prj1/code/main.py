import os
import math
import json
import pandas as pd
from collections import defaultdict
import gurobipy as gp
from gurobipy import GRB

ZIP_JSON = "./data/zipcodes.json" 
OUT_DIR = "./data/"

# ---------------------------------------
# 1) Load data from JSON and build inputs
# ---------------------------------------
def load_from_zip_json(path=ZIP_JSON):
    with open(path, "r") as f:
        data = json.load(f)
    all_zipcodes = sorted(set(data.keys()))

    # Collect ZIP-level parameters
    avg_income = {}
    emp_rate   = {}
    pop012     = {}
    pop05      = {}
    facilities = []

    for z in all_zipcodes:
        print(z)
        zipcode = data[z]
        inc_val = zipcode['avg_individual_income']['average income']
        emp_val = zipcode['employment_rate']['employment rate']
        p05 = zipcode['population']['-5']
        p012 = p05 + zipcode['population']['5-9'] + (3/5) * zipcode['population']['10-14']
        cap05 = zipcode['child_care_regulated']['infant_capacity'] + zipcode['child_care_regulated']['toddler_capacity'] + zipcode['child_care_regulated']['preschool_capacity']
        cap_total = zipcode['child_care_regulated']['total_capacity']

        avg_income[z] = float(inc_val)
        emp_rate[z]   = float(emp_val)
        pop012[z]     = float(p012)
        pop05[z]      = float(p05)

        # one pseudo facility per ZIP
        fid = f"fac_{z}"
        facilities.append({"fid": fid, "zip": z, "cap": cap_total, "cap05": cap05})

    return all_zipcodes, avg_income, emp_rate, pop012, pop05, facilities

# ------------------------------------------------
# 2) Build parameters from the policy description
# ------------------------------------------------
def build_parameters(zips_all, avg_income, emp_rate, facilities):
    S_types = ["S", "M", "L"]
    Cap_s   = {"S":100, "M":200, "L":400}
    Cap05_s = {"S":50,  "M":100, "L":200}
    Cost_s  = {"S":65000, "M":95000, "L":115000}

    beta  = 100
    theta = {}
    for z in zips_all:
        emp = float(emp_rate.get(z, 0))
        inc = float(avg_income.get(z, 1e9))
        theta[z] = 0.5 if (emp >= 60.0 or inc <= 60000.0) else (1.0/3.0)

    F_i = defaultdict(list)
    Cap_f = {}
    Cap05_f = {}                         

    for f in facilities:
        fid = f["fid"]
        z = f["zip"]
        F_i[z].append(fid)
        Cap_f[fid] = f['cap']
        Cap05_f[fid] = f["cap05"]

    return S_types, Cap_s, Cap05_s, Cost_s, beta, theta, F_i, Cap_f, Cap05_f

# ---------------------------
# 3) Build and solve the MILP
# ---------------------------
def build_and_solve(zips_all, pop012, pop05, S_types, Cap_s, Cap05_s, Cost_s,
                    beta, theta, F_i, Cap_f, Cap05_f):
    m = gp.Model("childcare_budget_min")

    x_f, u_f, z_f = {}, {}, {}
    y_is, v_is = {}, {}

    for z in zips_all:
        for fid in F_i[z]:
            cap = Cap_f[fid]
            ub = min(int(math.floor(0.2 * cap)), 500)
            x_f[fid] = m.addVar(vtype=GRB.INTEGER, lb=0, ub=ub, name=f"x_{fid}")
            u_f[fid] = m.addVar(vtype=GRB.INTEGER, lb=0, ub=ub, name=f"u_{fid}")
            z_f[fid] = m.addVar(vtype=GRB.BINARY, name=f"z_{fid}")

    for z in zips_all:
        for s in S_types:
            y_is[(z,s)] = m.addVar(vtype=GRB.INTEGER, lb=0, name=f"y_{z}_{s}")
            v_is[(z,s)] = m.addVar(vtype=GRB.INTEGER, lb=0, name=f"v_{z}_{s}")

    m.update()

    exp_cost = gp.quicksum((20000 + 200.0 * Cap_f[fid]) * z_f[fid] for fid in x_f)
    build_cost = gp.quicksum(Cost_s[s] * y_is[(z,s)] for z in zips_all for s in S_types)
    equip_cost = beta * (gp.quicksum(u_f[fid] for fid in u_f) + gp.quicksum(v_is[(z,s)] for z in zips_all for s in S_types))
    m.setObjective(exp_cost + build_cost + equip_cost, GRB.MINIMIZE)

    # Trigger and consistency
    for fid in x_f:
        m.addConstr(x_f[fid] >= Cap_f[fid] * z_f[fid], name=f"trigger_{fid}")
        m.addConstr(u_f[fid] <= x_f[fid], name=f"u_le_x_{fid}")

    for z in zips_all:
        for s in S_types:
            m.addConstr(v_is[(z,s)] <= Cap05_s[s] * y_is[(z,s)], name=f"v_le_cap05_{z}_{s}")

    # Overall coverage (all ages)
    for z in zips_all:
        lhs = gp.quicksum((Cap_f[fid] + x_f[fid]) for fid in F_i[z]) \
              + gp.quicksum(Cap_s[s] * y_is[(z,s)] for s in S_types)
        rhs = theta[z] * float(pop012.get(z, 0.0))
        m.addConstr(lhs >= rhs, name=f"coverage_{z}")

    # 0–5 coverage: include EXISTING 0–5 capacity
    for z in zips_all:
        existing_u5 = gp.quicksum(Cap05_f[fid] for fid in F_i[z])   # <-- existing under-5
        lhs = existing_u5 \
              + gp.quicksum(u_f[fid] for fid in F_i[z]) \
              + gp.quicksum(v_is[(z,s)] for s in S_types)
        rhs = (2.0/3.0) * float(pop05.get(z, 0.0))
        m.addConstr(lhs >= rhs, name=f"u5_coverage_{z}")

    m.Params.OutputFlag = 1
    m.optimize()

    if m.Status in [GRB.OPTIMAL, GRB.INTERRUPTED]:
        print("\n=== Optimal Objective (Minimum Total Budget) ===")
        print(f"Z* = ${m.ObjVal:,.2f}")
    else:
        print(f"Model ended with status {m.Status}.")

    # Outputs
    exp_rows = []
    for fid in x_f:
        xv = int(round(x_f[fid].X))
        uv = int(round(u_f[fid].X))
        zv = int(round(z_f[fid].X))
        z = next((zi for zi, fl in F_i.items() if fid in fl), None)
        exp_rows.append({
            "zip": z,
            "facility_id": fid,
            "cap_existing_total": Cap_f[fid],
            "cap_existing_u5": Cap05_f[fid],          # <-- include
            "expand_slots": xv,
            "expand_u5_slots": uv,
            "triggered_baseline": zv
        })
    pd.DataFrame(exp_rows).to_csv(os.path.join(OUT_DIR, "expansions.csv"), index=False)

    new_rows = []
    for z in zips_all:
        for s in S_types:
            yv = int(round(y_is[(z,s)].X))
            vv = int(round(v_is[(z,s)].X))
            if yv > 0 or vv > 0:
                new_rows.append({
                    "zip": z, "type": s, "build_count": yv, "u5_slots": vv,
                    "cap_per_facility": Cap_s[s], "cap05_per_facility": Cap05_s[s],
                    "cost_per_facility": Cost_s[s]
                })
    pd.DataFrame(new_rows).to_csv(os.path.join(OUT_DIR, "new_facilities.csv"), index=False)

    zip_rows = []
    for z in zips_all:
        total_existing_total = sum(Cap_f[fid] for fid in F_i[z])
        total_existing_u5    = sum(Cap05_f[fid] for fid in F_i[z])         
        total_expansion      = sum(int(round(x_f[fid].X)) for fid in F_i[z])
        built_slots          = sum(Cap_s[s] * int(round(y_is[(z,s)].X)) for s in S_types)
        total_slots          = total_existing_total + total_expansion + built_slots
        u5_total             = total_existing_u5 \
                               + sum(int(round(u_f[fid].X)) for fid in F_i[z]) \
                               + sum(int(round(v_is[(z,s)].X)) for s in S_types)
        zip_rows.append({
            "zip": z,
            "theta": theta[z],
            "pop_0_12": float(pop012.get(z, 0.0)),
            "pop_0_5": float(pop05.get(z, 0.0)),
            "slots_total": total_slots,
            "slots_u5": u5_total,                        
            "coverage_rhs": theta[z] * float(pop012.get(z, 0.0)),
            "u5_rhs": (2.0/3.0) * float(pop05.get(z, 0.0))
        })
    pd.DataFrame(zip_rows).to_csv(os.path.join(OUT_DIR, "zip_coverage.csv"), index=False)

    print(f"\nWrote results to: {OUT_DIR}/expansions.csv, {OUT_DIR}/new_facilities.csv, {OUT_DIR}/zip_coverage.csv")

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    zips_all, avg_income, emp_rate, pop012, pop05, facilities = load_from_zip_json(ZIP_JSON)
    S_types, Cap_s, Cap05_s, Cost_s, beta, theta, F_i, Cap_f, Cap05_f = build_parameters(
        zips_all, avg_income, emp_rate, facilities
    )
    build_and_solve(zips_all, pop012, pop05, S_types, Cap_s, Cap05_s, Cost_s,
                    beta, theta, F_i, Cap_f, Cap05_f)