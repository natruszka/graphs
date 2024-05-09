import random as rng
import networkx as nx
import prj3_zad1
import prj3_zad2
import numpy as np


ourgraph = prj3_zad1.RGraph()
ourgraph.randomize(vertice_count=10,edges_count=16)
graph = ourgraph.to_nxGraph()


print("N of nodes:", graph.number_of_nodes())
print("N of edges:", graph.number_of_edges())
print("Is connected:", nx.is_connected(graph))



#z3.zip
resultz3 = np.array([[ i[1]  for i in  sorted(list(nx.single_source_dijkstra(graph,node)[0].items()),key = lambda x : x[0]) ] for node in graph.nodes])
print(resultz3)
print()


#z3, but decompressed
resultz3 = []
for node in graph.nodes:
    res = prj3_zad2.Dijkstra(ourgraph,node)
    paths = prj3_zad2.Undijkstrify(res, node)
    lengths = prj3_zad2.Lengthify(paths, node , ourgraph.edges)
    resultz3.append(lengths)
    
resultz3 = np.array(resultz3)
print(resultz3)


#z4.zip
graph_center = min([(i,sum(distances)) for i, distances in enumerate(resultz3)],key=lambda x : x[1])
print('Centrum grafu:',graph_center)
graph_minmax = min([(i,max(distances)) for i, distances in enumerate(resultz3)],key=lambda x : x[1])
print('Minmax grafu:',graph_minmax)



