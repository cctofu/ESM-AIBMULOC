import gurobipy as gp
from gurobipy import GRB

model = gp.Model("Oil")

# Decision variables
x1 = model.addVar(vtype=GRB.INTEGER, name="crude_oil_method1", lb=0)
x2 = model.addVar(vtype=GRB.INTEGER, name="crude_oil_method2", lb=0)
x3 = model.addVar(vtype=GRB.INTEGER, name="crude_oil_method3", lb=0)
c1 = model.addVar(vtype=GRB.CONTINUOUS, name="cracked6_8", lb=0)
c2 = model.addVar(vtype=GRB.CONTINUOUS, name="cracked8_10", lb=0)
y1 = model.addVar(vtype=GRB.CONTINUOUS, name="grade6g", lb=0)
y2 = model.addVar(vtype=GRB.CONTINUOUS, name="grade8g", lb=0)
y3 = model.addVar(vtype=GRB.CONTINUOUS, name="grade10g", lb=0)
z1 = model.addVar(vtype=GRB.CONTINUOUS, name="grade6h", lb=0)
z2 = model.addVar(vtype=GRB.CONTINUOUS, name="grade8h", lb=0)
z3 = model.addVar(vtype=GRB.CONTINUOUS, name="grade10h", lb=0)

# Objective function
model.setObjective(12*(y1+y2+y3) + 5*(z1+z2+z3) - (3.4*x1 + 3.0*x2 + 2.6*x3) - (c1 + 1.5*c2), GRB.MAXIMIZE)

# Constraints
model.addConstr(y1 + y2 + y3 <= 2000, 'c1')
model.addConstr(z1 + z2 + z3 <= 600, 'c2')
model.addConstr(6*y1 + 8*y2 + 10*y3 >= 9*(y1 + y2 + y3), 'c3')
model.addConstr(6*z1 + 8*z2 + 10*z3 >= 7*(z1 + z2 + z3), 'c4')
model.addConstr(y1 + z1 == 0.3*x1 + 0.4*x2 + 0.1*x3 - c1, 'c5') 
model.addConstr(y2 + z2 == 0.5*x1 + 0.2*x2 + 0.3*x3 + c1 - c2, 'c6') 
model.addConstr(y3 + z3 == 0.8*x1 + 0.4*x2 + 0.2*x3 + c2, 'c7') 

model.optimize()
print(model.ObjVal)
for v in model.getVars():
    print(v.VarName, v.X)
