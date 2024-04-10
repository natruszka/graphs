import random as rng
import networkx as nx

def generate_connected_graph(node_n, edge_n):
    G = nx.Graph()
    G.add_nodes_from(range(node_n))

    while nx.number_connected_components(G) > 1:

        

        #degrees = [(node ,val) for (node, val) in G.degree()]
        #remaining = map(sum, map(lambda x : x[1] == 0 or x[1] == 1  ,degrees))
        #print(remaining)
        #print(degrees)

        node1, node2 = rng.sample(range(node_n),2)

        if not G.has_edge(node1, node2):
            G.add_edge(node1, node2,weight=rng.randint(0,10)+1)

    # Add remaining edges
    remaining_edges = edge_n - G.number_of_edges()
    for _ in range(remaining_edges):
        node1, node2 = rng.sample(range(node_n),2)
        if not G.has_edge(node1, node2):
            G.add_edge(node1, node2,weight=rng.randint(0,10)+1)

    return G


node_n = 10
edge_n = 15
graph = generate_connected_graph(node_n, edge_n)

print("N of nodes:", graph.number_of_nodes())
print("N of edges:", graph.number_of_edges())
print("Is connected:", nx.is_connected(graph))

#/\ to be removed




#z3.zip                                             \/ to be substituted
resultz3 = [[i[1]  for i in  sorted(list(nx.single_source_dijkstra(graph,node)[0].items()),key = lambda x : x[0]) ] for node in graph.nodes]
print(resultz3)

#z3, but decompressed
'''for node in graph.nodes:
    res = nx.single_source_dijkstra(graph,node)
    print(list(res[0].items()))
    print(sorted(list(res[0].items()),key = lambda x : x[0]))
    print(  [i[1]  for i in  sorted(list(res[0].items()),key = lambda x : x[0]) ]   )
'''

#z4.zip
graph_center = min([(i,sum(distances)) for i, distances in enumerate(resultz3)],key=lambda x : x[1])
print(graph_center)
graph_minmax = min([(i,max(distances)) for i, distances in enumerate(resultz3)],key=lambda x : x[1])
print(graph_minmax)



