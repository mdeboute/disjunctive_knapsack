from structures import *

# because Python 3.7 doesn't have the remove_suffix method for strings
def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def parser(filePath):
    # Exemple of .dat file:
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

    n = int(remove_suffix(lines[0].split(" ")[3], ";\n"))
    c = int(remove_suffix(lines[1].split(" ")[3], ";\n"))

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
        adjacency_matrix[int(line[1])][int(line[0])] = 1

    return Graph(n, adjacency_matrix, vertices_info), c