from utils import parser
from mip import *
import sys, time


def relax_kp(graph, c, u):
    n = graph.get_n()
    vertex = graph.get_vertices_info()

    model = Model(name='relax_kp', solver_name="CBC")
    model.verbose = 0

    x = [model.add_var(name="x_%s" % i, var_type=BINARY) for i in range(n)]

    model.objective = maximize(xsum(vertex[i].get_profit()*x[i] for i in range(n)) + u*(c - xsum(vertex[i].get_weight()*x[i] for i in range(n))))

    for i in range(n):
        for j in range(n):
            if i != j:
                if graph.get_adj_matrix()[i][j] == 1:
                    model.add_constr(x[i] + x[j] <= 1)

    model.optimize(max_seconds=2)

    return x

def find_u(graph, c, u2, u1=0, epsilon=1e-3):
    n = graph.get_n()
    vertex = graph.get_vertices_info()
    upsilon = (u1 + u2)/2
    upsilon_list = [upsilon]
    x = relax_kp(graph, c, upsilon)
    switch = True
    while switch == True:
        cx = xsum(vertex[i].get_weight()*x[i] for i in range(n)).x
        a = upsilon - epsilon
        b = upsilon + epsilon
        if cx > c:
            u1 = a
        elif cx < c:
            u2 = b
        upsilon = (u1 + u2)/2
        upsilon_list.append(upsilon)
        x = relax_kp(graph, c, upsilon)
        # if upsilon does not change anymore then stop (abs(cx-c) < epsilon is too strict)
        if abs(upsilon - upsilon_list[-2]) < epsilon:
            switch = False
        print(upsilon)

    return upsilon


if __name__ == "__main__":
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print("Usage: python3 src/relax_kp.py <fileName> <u> <e>")
        print("Where u is the upper bound of the upsilon variable.")
        print("Where e is the epsilon value. The precision of the upsilon.")
        exit(1)

    fileName = sys.argv[1]
    u2 = float(sys.argv[2])

    graph, c = parser(fileName)

    start = time.time()
    if len(sys.argv) == 4:
        e = float(sys.argv[3])
        u = find_u(graph, c, u2, epsilon=e)
    else:
        u = find_u(graph, c, u2)
    end = time.time()

    if u is not None:
        print("Result: %s" % u)
        print("Time: %s" % (end - start))
    else:
        print("No coef found!")
