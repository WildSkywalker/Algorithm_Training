def find_eulerian_tour(graph):
 #This function takes in a graph and determines if there exists an Eulerian tour. If yes, it will gives the tour in #term of an array of vertices in term of traveling order. If not, it will display a message and terminates the #program. The input format should be an array of numerical 2-tuples, indicating the edges in the graph.
 ######################
    


    
    def get_vetices_set(graph):
        #This function gets the vertex set from a given graph. Therefore we can use it to compute the degree of each #vertex and determine if a Eulerian tour exists.
        ########################

        vertex_set_dict={'x'}
        vertex_set=[]
        #Get the vertices from the first and second entry of input.
        vertex_first_entry={item[0] for item in graph}
        vertex_second_entry={item[1] for item in graph}
        #Update the info into the dictionary
        vertex_set_dict.update(vertex_first_entry)
        vertex_set_dict.update(vertex_second_entry)
        #Only dict can help us get unique elements. Now that is done, we convert our result to an array.
        for v in vertex_set_dict:
            vertex_set.append(v)

        vertex_set.remove('x')

        #print(vertex_set)

        return vertex_set

    def get_degree_vector(graph):
        #This function gives the vector of degrees corresponding to the result of the previous get_vertices_set #function.
        #########################
        

        #Get the vertex set first
        vertex_vector = get_vetices_set(graph)
        degree_vect=[]
        degree=0
        for i in vertex_vector:
            connect_edges=[neihbour for neihbour in graph if i in neihbour]
            degree=len(connect_edges)
            #Count the number of self loops attached to vertex i and adjust the degree to the correct value.
            #A self loop is counted twice towards the degree.
            degree=degree+graph.count((i,i))
            #Add the degree of vertex i to the vector.
            degree_vect.append(degree)
        
        #print(degree_vect)

        return degree_vect


    def is_connected(graph):
        #This function checks if a given graph is connected.
    

        total_vertices=len(get_vetices_set(graph))
        #get the total number of vertices first, as the input graph will be changed later on.
        current_vertex=graph[0][0]
        #current_vertex is the current location in the algorithn
        active_vertex=[graph[0][0]]
        #active_vertex is the array of active vertices.
        cluster=0
        #Number of vertices in current cluster.
        connectedness=0
        #connectedness is the value representing whether the graph is connected.      
        current_vertex_loop=0
        #This temp counter is for removing loops. However, we cannot remove all loops at the beginning. Imagine we #have a graph consist of only self loops. Removing all of them will set total_edge to 0 and we get a connected #a graph, which is obviously wrong.
        while len(active_vertex) > 0:
            #Count the loop of the current vertex and remove them
            current_vertex_loop=graph.count((current_vertex,current_vertex))
            for i in range(current_vertex_loop):
                    graph.remove((current_vertex,current_vertex))

            #################
            #Now start exploring and get neihbour.

            #First, if there is no connected edge to the current vertex. Remove that from the active vertice pool, increase the cluster size by 1, and move onto the next active vertex.
            connect_edges=[neihbour for neihbour in graph if current_vertex in neihbour]
            if len(connect_edges) == 0:
                active_vertex.remove(current_vertex)
                cluster=cluster+1
                #print(cluster)
                if len(active_vertex) == 0:
                    continue
                current_vertex=active_vertex[0]
                continue
            #If every active vertex has no connected edges, we are coming to the end of the searching algorithm. #Compare the cluster and the total numer of vertices and get the result.
            #The if inside the for loop also avoided adding same copies of a single vertex multiple times if there are #multi-edges.
            for edge in connect_edges:
                if edge[0] == current_vertex and active_vertex.count(edge[1]) == 0:
                    active_vertex.append(edge[1])
                elif edge[1] == current_vertex and active_vertex.count(edge[0]) == 0:
                    active_vertex.append(edge[0])
            #print(active_vertex)
            #Remove every edge that connects to the current vertex. The arguments below remove every mutli-edge.
            #Also we consdier different input format. For example, if a is the current vertex. Then both (a,b) and
            #(b,#a) will be removed.
            for vertex in active_vertex:
                order1 = graph.count((current_vertex,vertex))
                for k in range(order1):
                    graph.remove((current_vertex,vertex))
                order2 = graph.count((vertex,current_vertex))
                for k_prime in range(order2):
                    graph.remove((vertex,current_vertex))
            #Remove the current vertex from the active vertices pool.  
            active_vertex.remove(current_vertex)   
            #print(active_vertex)   
            #Move current vertex to the next active vertex and update the size of the cluster.
            current_vertex=active_vertex[0]
            #print(current_vertex)
            #Now we explore all the neibours of the current vertex. Increase cluster size by 1
            cluster=cluster+1
            
        #Check the result.
        if cluster == total_vertices:
            connectedness = 1
        # else:
        #     print("The graph is not connected")
        #     print("The cluster size of the first vertex is ",cluster)
        return connectedness

    def is_Eulerian(graph_input):
        #This function determines if a Eulerian tour exists in the given graph.
        ######################


        degree_vect_mod2=[j%2 for j in get_degree_vector(graph_input)]
        #Count the number of odd degree vertices in the graph.
        odd_deg_vertices=degree_vect_mod2.count(1)
        #eulerian_status gives the result whether the given graph has a eulerian tour. In mathematics, a graph has a #Eulerian Tour if and #only if the number of odd vertices is smaller or equal to two.
        #eulerian_status = 1 means the graph has no odd degree vertices. A Eulerian tour can start at any point.
        #eulerian_status = 2 means the graph has two odd degree vertices. A Eulerian tour can only start at one of them and end at the other.
        eulerian_status=0
        if is_connected(graph_input) == 0:
            
            eulerian_status=0
        elif odd_deg_vertices > 3:
            eulerian_status=-1
        else:
            eulerian_status=1

        return eulerian_status    


    def generate_Eulerian_tour(graph):
        #This function uses the Fleury's algorithm to generate the eulerian tour. See
        #https://en.wikipedia.org/wiki/Eulerian_path#Fleury's_algorithm

        The_Grand_Tour=[]
        #Pertrol head.. why not? XD

        #Get the collection of vertices and their degrees mod 2.
        vertex_set=get_vetices_set(graph)
        vertex_deg=[l%2 for l in get_degree_vector(graph)]
        #Get the total number of edges.
        total_edges=len(graph)
        #Determine if there are odd degree vertices. If so, the Eulerian path must start at the odd vertices.
        odd_number=vertex_deg.count(1)
        #If every vertex has even degree, then we just choose the first one as our starting point.
        if odd_number == 0:
            current_vertex = vertex_set[0]
        else:
            start_index=vertex_deg.index(1)
            current_vertex=vertex_set[start_index]
        

        #Initiate the Eulerian tour.
        The_Grand_Tour.append(current_vertex)


        while total_edges>0:
        #Find connected edges
            connected_edges = [neihbour for neihbour in graph if current_vertex in neihbour]
            #Count the self-loop of the current vertex.
            current_self_loop = connected_edges.count((current_vertex,current_vertex))
            for i in range(current_self_loop):
                The_Grand_Tour.append(current_vertex)
                graph.remove((current_vertex,current_vertex))
                total_edges=total_edges-1
                connected_edges.remove((current_vertex,current_vertex))
            
            #If there is only one remaining edge, that means we are at the end of the tour. Finish the tour and break the loop.
            if total_edges == 1:
                edge=connected_edges[0]
                if edge[0] == current_vertex:
                    current_vertex=edge[1]
                else:
                    current_vertex=edge[0]
                total_edges=total_edges-1
                The_Grand_Tour.append(current_vertex)
                graph.remove(edge)
                print(The_Grand_Tour)
                return The_Grand_Tour
            else:
                #If we are not at the end, here is when the algorithm comes in. Remove an edge such that the graph remains connected.
                for edge in connected_edges:
                    graph_temp=graph[:]
                    graph_temp.remove(edge)
                    #Check if remove the current edge will maintain the connectivity of the graph.
                    if is_connected(graph_temp) == 1:
                        #If that is the case, remove the edge, update the tour, break the loop, and move on.
                        if edge[0] == current_vertex:
                            current_vertex=edge[1]
                        else:
                            current_vertex=edge[0]
                        total_edges=total_edges-1
                        The_Grand_Tour.append(current_vertex)
                        graph.remove(edge)
                        break


    ######################
    ######################
    ###Program Main Body####
    #First determine if the input graph has an Eulerian tour.
    #Get a copy of the input graph, because the input graph will be altered during the connectivity test.
    #Notice that we cannot use graph_copy=graph, since it will simply binds this variable with graph, and it will change with graph.
    #We have to use graph_copy=graph[:]
    graph_copy=graph[:]
    status=is_Eulerian(graph_copy)
    if status == 0:
        print("The graph is not connected.")
        return
    elif status == -1: 
        print("This does not exist an Eulerian tour in the graph.")
        return
    else:
        #Now we know there exists a tour. Use the function to generate the path.
        print("We have a Eulerian Graph. The Eulerian Tour is:")
        final_tour=generate_Eulerian_tour(graph)
        return final_tour

find_eulerian_tour([(1,1),(1,1),(1,2),(1,2),(3,1),(3,1),(2,4),(4,5)])
