from utils import parser
from mip import *
import sys, time


def calc_disj_expression(graph, v, x):
    n = graph.get_n()
    disj_expression = 0
    for i in range(n):
        for j in range(n):
            if i != j and graph.get_adj_matrix()[i][j] == 1:
                disj_expression = disj_expression + v[i][j] * (x[i] + x[j] - 1)
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

    #model.optimize(max_seconds=2)
    model.optimize()

    return x, model


def indexesSortedByProfit(vertex):
    n = len(vertex)
    I = [i for i in range(n)]
    J = []
    while len(J) < n:
        max_val = -1
        max_i = -1
        for i in I:
            val = vertex[i].get_profit() / vertex[i].get_weight()
            if val > max_val:
                max_val = val
                max_i = i
        I.remove(max_i)
        J.append(max_i)
    return J


# Fonction glouton pour trouver une solution réalisable pour le problème d'origine
# qui servira de borne supérieure au problème.
def upper_bound(graph, c):
    n = graph.get_n()
    vertex = graph.get_vertices_info()
    I = indexesSortedByProfit(vertex)
    ub = 0
    cx = 0
    while len(I) > 0:
        i = I[len(I) - 1]
        if cx + vertex[i].get_weight() < c:
            ub = ub - vertex[i].get_profit()
            cx += vertex[i].get_weight()

            for j in range(n):
                if i != j and graph.get_adj_matrix()[i][j] == 1 and j in I:
                    I.remove(j)
        I.pop()
    return ub


def sub_gradient(graph, x):
    n = graph.get_n()
    s = []
    for i in range(n):
        for j in range(n):
            if i != j and graph.get_adj_matrix()[i][j] == 1:
                s.append((x[i].x + x[j].x - 1)**2)
    return sum(s)


def find_v(graph, c, alpha=1e-2, epsilon=1e-2):
    """
    It's a subgradient algorithm to find the best v coefficient
    to solve the Lagrangian dual problem of the Disjunctive relax KP MILP.
    """
    n = graph.get_n()
    ub = upper_bound(graph, c)

    v = [[0 for j in range(n)] for i in range(n)]
    v_prec = [[-1 for j in range(n)] for i in range(n)]

    x, model = relax_disj(graph, c, v)
    subGradient = [sub_gradient(graph, x)]
    if subGradient[-1] == 0:
        return v
    has_improved = True
    while has_improved:
        s = alpha * (ub - model.objective_value) / subGradient[-1]
        has_improved = False
        for i in range(n):
            for j in range(n):
                if i != j and graph.get_adj_matrix()[i][j] == 1:
                    #s = 0
                    #if ((x[i].x + x[j].x - 1)!=0):
                    #    s = alpha * (ub - model.objective_value) / ((x[i].x + x[j].x - 1) ** 2)

                    if abs(v_prec[i][j] - v[i][j]) > epsilon:
                        
                        #print(v_prec[i][j] , v[i][j], end="   ")
                        v_prec[i][j] = v[i][j]
                        v[i][j] = max(0, v[i][j] + s * (x[i].x + x[j].x - 1))
                        if abs(v_prec[i][j] - v[i][j]) > epsilon:
                            print(s, "   ", (x[i].x + x[j].x - 1), "   " , v_prec[i][j] , v[i][j])
                            has_improved = True

        x, model = relax_disj(graph, c, v)
        if (model.status == OptimizationStatus.INFEASIBLE):
            for i in range(n):
                for j in range(n):
                    if i != j and graph.get_adj_matrix()[i][j] == 1:
                        if v[i][j]!=0:
                            print(v[i][j])
        subGradient.append(sub_gradient(graph, x))
        if subGradient[-1] == 0:
            break

    return v


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: relax_disj.py <fileName>")
        exit(1)

    fileName = sys.argv[1]
    graph, c = parser(fileName)
    n = graph.get_n()

    start = time.time()
    v = find_v(graph, c)
    end = time.time()

    if v is not None:
        print("Result: v = %s" % v)
        print("Time: %s" % (end - start))

        x, model = relax_disj(graph, c, v)
        if model.status == OptimizationStatus.OPTIMAL:
            print("Relaxed model objective value:", model.objective_value)
            vertex = graph.get_vertices_info()
            profit = xsum(vertex[i].get_profit() * x[i] for i in range(n)).x
            weight = xsum(vertex[i].get_weight() * x[i] for i in range(n)).x
            print("Constraint: Total weight =", weight, ", Capacity =", c)
            print("Original model objective value:", profit)
