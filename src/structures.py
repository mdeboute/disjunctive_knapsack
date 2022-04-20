class Vertex:
    def __init__(self, id, profit, weight):
        self.id = id
        self.profit = profit
        self.weight = weight

    def __str__(self):
        return f"{self.id} {self.profit} {self.weight}"

    def __repr__(self):
        return f"{self.id} {self.profit} {self.weight}"

    def __eq__(self, other):
        return self.id == other.id and self.profit == other.profit and self.weight == other.weight

    def __hash__(self):
        return hash(self.id) ^ hash(self.profit) ^ hash(self.weight)

    def get_id(self):
        return self.id

    def get_profit(self):
        return self.profit

    def get_weight(self):
        return self.weight


class Graph:
    def __init__(self, n, adjacency_matrix, vertices_info):
        self.n = n
        self.adj_matrix = adjacency_matrix
        self.vertices_info = vertices_info

    def __eq__(self, other):
        return self.n == other.n and self.adj_matrix == other.adj_matrix and self.vertices_info == other.vertices_info

    def __hash__(self):
        return hash(self.n) ^ hash(self.adj_matrix) ^ hash(self.vertices_info)

    def get_n(self):
        return self.n

    def get_adj_matrix(self):
        return self.adj_matrix

    def get_vertices_info(self):
        return self.vertices_info




