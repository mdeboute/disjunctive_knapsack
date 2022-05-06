from utils import parser
from mip import *
import sys, time


def relax_kp(graph, c, u):
    n = graph.get_n()
    vertex = graph.get_vertices_info()

    model = Model(name="relax_kp", solver_name="CBC")
    model.verbose = 0

    x = [model.add_var(name="x_%s" % i, var_type=BINARY) for i in range(n)]

    model.objective = maximize(
        xsum(vertex[i].get_profit() * x[i] for i in range(n))
        + u * (c - xsum(vertex[i].get_weight() * x[i] for i in range(n)))
    )

    for i in range(n):
        for j in range(n):
            if i != j:
                if graph.get_adj_matrix()[i][j] == 1:
                    model.add_constr(x[i] + x[j] <= 1)
                    
    #model.optimize(max_seconds=2)
    model.optimize()

    return x, model


def find_u(graph, c, epsilon=1e-3):
    """
    It's a dichotomic search to find the best upsilon coefficient
    to solve the Lagrangian dual problem of the Disjunctive relax KP MILP.

    First we start from u_max = 1 and slowly raise it to find an upper bound for u,
    then we do a dichotomic search for the optimal u between u_max and u.
    """

    n = graph.get_n()
    vertex = graph.get_vertices_info()
    u_prec = 0
    u_max = 1
    x, model = relax_kp(graph, c, u_max)
    while model.status == OptimizationStatus.OPTIMAL:
        print(u_max)
        constr = c - xsum(vertex[i].get_weight() * x[i] for i in range(n)).x
        if constr==0:
            return u_max
        elif constr < 0:
            u_prec = u_max
            u_max = u_max * 2
            x, model = relax_kp(graph, c, u_max)
        else:
            break;
    u1 = u_prec
    u2 = u_max

    upsilon = (u1 + u2) / 2
    upsilon_list = [u_prec, upsilon]
    x, model = relax_kp(graph, c, upsilon)

    switch = True
    while model.status == OptimizationStatus.OPTIMAL:
        cx = xsum(vertex[i].get_weight() * x[i] for i in range(n)).x
        print("u =", upsilon, ", cx =", cx)
        # if upsilon does not change anymore then stop (abs(cx-c) < epsilon is too strict
        if abs(upsilon - upsilon_list[-2]) <= epsilon and cx <= c:
            break;
        a = upsilon - epsilon
        b = upsilon + epsilon
        #a = upsilon
        #b = upsilon
        if cx > c:
            u1 = a
        elif cx < c:
            u2 = b
        else: # cx==c (contrainte respectée et solution optimale pour les deux problèmes)
            print("constraint satisfied!")
            break;
        upsilon = (u1 + u2) / 2
        upsilon_list.append(upsilon)
        x, model = relax_kp(graph, c, upsilon)

    return upsilon


if __name__ == "__main__":
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        print("Usage: python3 src/relax_kp.py <fileName> <e>")
        #print("Where u is the upper bound of the upsilon variable.")
        print("Where e (optional) is the epsilon value. The precision of the upsilon.")
        exit(1)

    fileName = sys.argv[1]

    graph, c = parser(fileName)
    n = graph.get_n()

    start = time.time()
    if len(sys.argv) == 3:
        e = float(sys.argv[2])
        u = find_u(graph, c, epsilon=e)
    else:
        u = find_u(graph, c)
    end = time.time()

    if u is not None:
        print("Result: u = %s" % u)
        print("Time: %s" % (end - start))

        x, model = relax_kp(graph, c, u)
        if model.status == OptimizationStatus.OPTIMAL:
            print("Relaxed model objective value:", model.objective_value)
            vertex = graph.get_vertices_info()
            profit = xsum(vertex[i].get_profit() * x[i] for i in range(n)).x
            weight = xsum(vertex[i].get_weight() * x[i] for i in range(n)).x
            print("Constraint: Total weight =", weight, ", Capacity =", c)
            print("Original model objective value:", profit)
    else:
        print("No coeff found!")
