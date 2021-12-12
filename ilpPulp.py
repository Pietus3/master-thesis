from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

model = LpProblem(name="small-problem", sense=LpMaximize)

x1 = LpVariable(name="x1",lowBound = 0,cat="Binary")
x2 = LpVariable(name="x2",lowBound = 0,cat="Binary")
x3 = LpVariable(name="x3",lowBound = 0,cat="Binary")
y1 = LpVariable(name="y1",lowBound = 0,cat="Binary")
y2 = LpVariable(name="y2",lowBound = 0,cat="Binary")
z1 = LpVariable(name="z1",lowBound = 0,cat="Binary")


# Add the constraints to the model
model += (x1*0.8+x2*0.3+0.1*x3 <= 1, "red_constraint")
model += (x1*0.8+x2*0.3+0.1*x3 +y1*0.2+y2*0.1 <= 1, "blue_constraint")
model += (x1*0.8+x2*0.3+0.1*x3 +y1*0.2+y2*0.1 + z1*0.1 <= 1, "yellow_constraint")
model += (x1+x2+x3== 1, "xsum")
model += (y1+y2== 1, "ysum")
model += (z1== 1, "zsum")

# Add the objective function to the model
obj_func = x1*0.5+x2*0.3+x3*0.2+y1*0.4+y2*0.1+z1*0.2
model += obj_func

print(model)

status  =model.solve()

print(f"status: {model.status}, {LpStatus[model.status]}")


print(f"objective: {model.objective.value()}")


for var in model.variables():
    print(f"{var.name}: {var.value()}")