from utils import parser
from mip import *
import sys, time


def relax_disj(graph, c, v):
    n = graph.get_n()
    vertex = graph.get_vertices_info()

    model = Model(name='relax_disj', solver_name="CBC")
    model.verbose = 0

    x = [model.add_var(name="x_%s" % i, var_type=BINARY) for i in range(n)]

    disj_expression = 0
    for i in range(n):
        for j in range(n):
            if i != j and graph.get_adj_matrix()[i][j] == 1:
                disj_expression += v[i][j]*(1-x[i]-x[j])

    model.objective = maximize(xsum(vertex[i].get_profit()*x[i] for i in range(n)) + disj_expression)

    model.add_constr(xsum(vertex[i].get_weight()*x[i] for i in range(n)) <= c)

    model.optimize(max_seconds=2)

    return x, model

def calc_disj_expression(graph, v, x):
    n = graph.get_n()
    disj_expression = 0
    for i in range(n):
        for j in range(n):
            if i != j and graph.get_adj_matrix()[i][j] == 1:
                disj_expression += v[i][j]*(1-x[i]-x[j])
    return disj_expression

def find_v(graph, c, v, alpha=1, epsilon=1e-3):
    """
    It's a subgradient algorithm to find the best phi coefficient
    to solve the Lagrangian dual problem of the Disjunctive relax KP MILP.
    """

    x, model = relax_disj(graph, c, v)
    thetas = [model.objective_value]

    if model.status == OptimizationStatus.OPTIMAL:
        return v

    phi = v

    switch = True
    while switch == True:
        lb = thetas[-1]
        disj_expression = calc_disj_expression(graph, v, x)
        s = alpha*(lb-thetas[-1])/(abs(disj_expression)**2)
        phi = phi + s*disj_expression
        x, model = relax_disj(graph, c, v=phi)
        thetas.append(model.objective_value)
        if model.status == OptimizationStatus.OPTIMAL:
            switch = False
        if abs(thetas[-1] - thetas[-2]) < epsilon:
            switch = False
        print(phi)

    return phi


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: relax_kp.py <fileName>")
        exit(1)

    fileName = sys.argv[1]

    graph, c = parser(fileName)
    n = graph.get_n()
    v = [[0 for i in range(n)] for j in range(n)]

    start = time.time()
    v = find_v(graph, c, v)
    end = time.time()

    if v is not None:
        print("Result: %s" % v)
        print("Time: %s" % (end - start))
    else:
        print("No coeff found!")
