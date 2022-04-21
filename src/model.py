from utils import parser
from mip import *
import sys, time


if len(sys.argv) < 3 or len(sys.argv) > 3:
    print("Bad number of arguments!")
    print("Usage: python3 model.py <input_file> <output_dir>")
    sys.exit()

data_file = sys.argv[1]
output_dir = sys.argv[2]

graph, c = parser(data_file)

n = graph.get_n()
vertex = graph.get_vertices_info()

model = Model(name='disjunctive_knapsack', solver_name="CBC")
model.verbose = 0

x = [model.add_var(name="x_%s" % i, var_type=BINARY) for i in range(n)]

model.objective = maximize(xsum(vertex[i].get_profit()*x[i] for i in range(n)))

model.add_constr(xsum(vertex[i].get_weight()*x[i] for i in range(n)) <= c)

for i in range(n):
    for j in range(n):
        if i != j:
            if graph.get_adj_matrix()[i][j] == 1:
                model.add_constr(x[i] + x[j] <= 1)

start = time.perf_counter()
status = model.optimize(max_seconds=30)
runtime = time.perf_counter() - start

if data_file.__contains__("/"):
    data_file = data_file.split("/")[-1]

data_file = data_file.removesuffix(".dat")
sol_file = output_dir + data_file + ".sol"

with open(sol_file, 'w') as file:
    if status == OptimizationStatus.OPTIMAL:
        file.write("Resolution status: OPTIMAL")
    elif status == OptimizationStatus.FEASIBLE:
        file.write("Resolution status: TIMED OUT and CALCULATED FEASIBLE SOLUTION")
    elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        file.write("Resolution status: TIMED OUT and NO SOLUTION FOUND")
    elif status == OptimizationStatus.INFEASIBLE or status == OptimizationStatus.INT_INFEASIBLE:
        file.write("Resolution status: INFEASIBLE")
    elif status == OptimizationStatus.UNBOUNDED:
        file.write("Resolution status: UNBOUNDED")

    file.write("\nResolution time (sec) : " + str(round(runtime, 3))+"\n")
    file.write("----------------------------------\n")

    if model.num_solutions > 0:
        file.write("Result; " + data_file + "; " + str(round(runtime, 3)) + "; " + str(status) + "; " + str(model.objective_value) +"\n")
    else:
        file.write("Result; " + data_file + "; " + str(round(runtime, 3)) + "; " + str(status) + "; No solution returned!\n")

    file.close()
