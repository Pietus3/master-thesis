from scipy.optimize import linprog

obj = [-0.5, -0.3,-0.2,-0.4,-0.2,-0.3]
#      ─┬  ─┬
#       │   └┤ Coefficient for y
#       └────┤ Coefficient for x

lhs_ineq = [[ 2,0.3,0.2,0,0,0],  # Red constraint left side
             [ 2,0.3,0.2,0.4,0.2,0],  # Blue constraint left side
            [ 2,0.3,0.2,0.4,0.2,0.2]]  # Yellow constraint left side

rhs_ineq =  [1,  # Red constraint right side
             1,  # Blue constraint right side
              1]  # Yellow constraint right side

lhs_eq = [[1,1,1,0,0,0],[0,0,0,1,1,0],[0,0,0,0,0,1]]  # Green constraint left side
rhs_eq = [1,1,1]       # Green constraint right side

bnd = [(0, float("inf")),
       (0, float("inf")),
       (0, float("inf")),
(0, float("inf")),
(0, float("inf")),  # Bounds of x
       (0, float("inf"))]  # Bounds of y


opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
              A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
              method="revised simplex")

print(opt)