from structures import *

def parser(filePath):
    # Ewemple of .dat file:
    # param n := 500;
    # param c := 1000;
    # param : V : p w :=
    #    0	  11	   1
    #    ...
    #    499  110	   100
    # ;
    # set E :=
    #    0	  53
    #    ...
    #    480  481
    # ;

    """
    Parse the file and returns: G, c
    With G := {n, V, E} where V is a list of Vertex objects and E is an adjacency matrix.
    """

    with open(filePath, "r") as f:
        lines = f.readlines()

    n = int(lines[0].split(" ")[3].removesuffix(";\n"))
    c = int(lines[1].split(" ")[3].removesuffix(";\n"))

    vertices_info = list()
    for line in lines[3:n+3]:
        # remove \t and extra spaces
        line = line.replace("\t", " ").strip()
        # split by space and remove empty strings
        line = [x for x in line.split(" ") if x != ""]
        vertices_info.append(Vertex(int(line[0]), int(line[1]), int(line[2])))

    adjacency_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for line in lines[n+6:-1]:
        # remove \t and extra spaces
        line = line.replace("\t", " ").strip()
        # split by space and remove empty strings
        line = [x for x in line.split(" ") if x != ""]
        adjacency_matrix[int(line[0])][int(line[1])] = 1

    return Graph(n, adjacency_matrix, vertices_info), c