from utils import parser
from mip import *
import sys, time, math


def calc_disj_expression(graph, v, x):
    n = graph.get_n()
    disj_expression = 0
    for i in range(n):
        for j in range(n):
            if i != j and graph.get_adj_matrix()[i][j] == 1:
                disj_expression += v[i] * (1 - x[i] - x[j])
    return disj_expression


def relax_disj(graph, c, v):
    n = graph.get_n()
    vertex = graph.get_vertices_info()

    model = Model(name="relax_disj", solver_name="CBC")
    model.verbose = 0

    x = [model.add_var(name="x_%s" % i, var_type=BINARY) for i in range(n)]

    disj_expression = calc_disj_expression(graph, v, x)

    model.objective = minimize(
        xsum(-vertex[i].get_profit() * x[i] for i in range(n)) + disj_expression
    )

    model.add_constr(xsum(vertex[i].get_weight() * x[i] for i in range(n)) <= c)

    model.optimize(max_seconds=2)

    return x, model


def sub_gradient(graph, x):
    n = graph.get_n()
    s = []
    for i in range(n):
        for j in range(n):
            if i != j and graph.get_adj_matrix()[i][j] == 1:
                s.append(1 - x[i].x - x[j].x)
    return sum(s)


def L(x, v):
    # TODO: l(v) = cx + v(b-Ax)
    return


def find_v(graph, c, alpha=1, epsilon=1e-3):
    """
    It's a subgradient algorithm to find the best v coefficient
    to solve the Lagrangian dual problem of the Disjunctive relax KP MILP.
    """

    n = graph.get_n()
    v = [0 for _ in range(n)]
    x, model = relax_disj(graph, c, v)
    ub = [model.objective_value]
    subGradient = [sub_gradient(graph, x)]
    if subGradient[-1] == 0:
        return v
    while True:
        s = (alpha * (ub[-1] - L(x, v))) / (abs(subGradient[-1]) ** 2)
        v = (
            v + s * subGradient[-1]
        )  # TODO: find a way to multipply a vector by a scalar in python
        print(v)
        x, model = relax_disj(graph, c, v)
        ub.append(model.objective_value)
        subGradient.append(sub_gradient(graph, x))
        if abs(ub[-1] - ub[-2]) < epsilon:
            break
        if subGradient[-1] == 0:
            break

    return subGradient


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: relax_kp.py <fileName>")
        exit(1)

    fileName = sys.argv[1]
    graph, c = parser(fileName)

    v = find_v(graph, c)
    print(v)
