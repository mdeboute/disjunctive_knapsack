from utils import parser
import sys, time


if __name__ == "__main__":
    fileName = sys.argv[1]
    graph, c = parser(fileName)
    n = graph.get_n()
    vertex = graph.get_vertices_info()

    profits = []
    for i in range(n):
        profits.append(vertex[i].get_profit())

    weights = []
    for i in range(n):
        weights.append(vertex[i].get_weight())

    # create a two-dimensional array of n+1 rows and c+1 columns
    matrix = [[0 for x in range(c + 1)] for y in range(n + 1)]

    start = time.time()

    for item in range(1, n + 1):
        for capacity in range(1, c + 1):
            maxValWithoutCurr = matrix[item - 1][capacity]
            maxValWithCurr = 0

            weightOfCurr = weights[item - 1]
            if capacity >= weightOfCurr:
                maxValWithCurr = profits[item - 1]

                remainingCapacity = capacity - weightOfCurr
                maxValWithCurr += matrix[item - 1][remainingCapacity]

            matrix[item][capacity] = max(maxValWithoutCurr, maxValWithCurr)

    print(
        f"Dynamic programming solution cost: {matrix[n][c]}, in {time.time() - start} seconds"
    )

    from relax_disj import relax_disj

    start = time.time()

    x, model = relax_disj(graph, c, v=[[0 for i in range(n)] for j in range(n)])
    print(
        f"Relaxed MILP solution cost: {-model.objective_value}, in {time.time() - start} seconds"
    )  # minus because of minimization
