import random as rng
import networkx as nx
import prj3_zad1
import prj3_zad2
import numpy as np


graph = prj3_zad1.RGraph()
graph.randomize(vertice_count=10,edges_count=16)
graph = graph.to_nxGraph()


print("N of nodes:", graph.number_of_nodes())
print("N of edges:", graph.number_of_edges())
print("Is connected:", nx.is_connected(graph))



#z3.zip
resultz3 = np.array([[ i[1]  for i in  sorted(list(nx.single_source_dijkstra(graph,node)[0].items()),key = lambda x : x[0]) ] for node in graph.nodes])
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



