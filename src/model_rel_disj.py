from utils import parser
from mip import *
import sys, time


if len(sys.argv) != 2:
    print("Bad number of arguments!")
    print("Usage: python3 model.py <input_file>")
    sys.exit()

data_file = sys.argv[1]
graph, c = parser(data_file)
n = graph.get_n()
vertex = graph.get_vertices_info()
v = [[0 for j in range(n)] for i in range(n)]

model = Model(name='disjunctive_knapsack_relax', solver_name="CBC")
# model.verbose = 0

x = [model.add_var(name="x_%s" % i, var_type=BINARY) for i in range(n)]

disj_expression = 0
for i in range(n):
    for j in range(n):
        if i != j and graph.get_adj_matrix()[i][j] == 1:
            disj_expression += v[i][j]*(1-x[i]-x[j])

model.objective = maximize( xsum(vertex[i].get_profit()*x[i] for i in range(n)) + disj_expression )

model.add_constr(xsum(vertex[i].get_weight()*x[i] for i in range(n)) <= c)

start = time.perf_counter()
status = model.optimize(max_seconds=30)
runtime = time.perf_counter() - start

if data_file.__contains__("/"):
    data_file = data_file.split("/")[-1]

if status == OptimizationStatus.OPTIMAL:
    print("Resolution status: OPTIMAL")
elif status == OptimizationStatus.FEASIBLE:
    print("Resolution status: TIMED OUT and CALCULATED FEASIBLE SOLUTION")
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print("Resolution status: TIMED OUT and NO SOLUTION FOUND")
elif status == OptimizationStatus.INFEASIBLE or status == OptimizationStatus.INT_INFEASIBLE:
    print("Resolution status: INFEASIBLE")
elif status == OptimizationStatus.UNBOUNDED:
    print("Resolution status: UNBOUNDED")

print("\nResolution time (sec) : " + str(round(runtime, 3))+"\n")
print("----------------------------------\n")

if model.num_solutions > 0:
    print("Result; " + data_file + "; " + str(round(runtime, 3)) + "; " + str(status) + "; " + str(model.objective_value) +"\n")
else:
    print("Result; " + data_file + "; " + str(round(runtime, 3)) + "; " + str(status) + "; No solution returned!\n")
