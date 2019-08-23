import numpy
def create_tour(nodes):
    #This programs take an array and generate a graph that has a Eulerian path.
    #Since we are not required to generate all possible graphs with given nodes but only one, we shall create the
    #simplist graph, which is just a loop by connecting nodes one after another.

    #First, get the length of the array.
    vertices_number = len(nodes)
    #declare the resulting graph
    result_graph = []

    for i in range(0,vertices_number-1):
        result_graph.append(tuple((nodes[i],nodes[i+1])))
    #Finally, append the tuple consist of the last and the first vertex.
    result_graph.append(tuple((nodes[vertices_number-1],nodes[0])))
    print(result_graph)
    return result_graph

create_tour([5,6,7,8])
