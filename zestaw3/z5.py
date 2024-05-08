import prj3_zad1
import networkx as nx
import matplotlib.pyplot as plt

'''
graph = [
  [0,0,5,1],
  [0,0,4,6],
  [5,4,0,10],
  [1,6,10,0]
]

graph = [
  [0,0,5,1,7],
  [0,0,4,6,2],
  [5,4,0,10,0],
  [1,6,10,0,0],
  [7,2,0,0,0]
]'''


graph = prj3_zad1.RGraph()
graph.randomize(vertice_count=10,edges_count=16)
nxgraph = graph.to_nxGraph()
graph = nx.adjacency_matrix(nxgraph).toarray()

print(graph)


elem = range(len(graph))
edges = []

for i in range(len(graph)):
  for j in range(i):
    if graph[i][j] > 0:
      edges.append((set((i+1,j+1)),graph[i][j]) )


tree_set = [{i+1} for i in range(len(graph))]
edge_set = []


while len(tree_set) != 1:
  edges.sort(key=lambda x : x[1])
  direction = edges[0]




  #spaghetti section
  connection = []
  for target in tree_set:
    intersection = direction[0].intersection(target)
    if len(intersection) == 2: #tworzy cykl
      break
    elif len(intersection) == 1: #nie tworzy cyklu, ale jest fragment w znalezionym drzewie - zbieram do przetworzenia
      connection.append(target)
  else: #nie powoduje powstania cyklu - przylaczamy
    edge_set.append(edges[0])
    tree_set.remove(connection[0]) #wylapane wczesniej drzewa tu wykorzystujemy
    tree_set.remove(connection[1])
    tree_set.append(connection[0].union(connection[1])) #i laczymy oba drzewa
  edges.pop(0)
  #print(edge_set)
  #print(tree_set)
  #print()
  
print(edge_set)
print(tree_set)




result = nx.Graph()

for (x, cost) in edge_set:
  x = list(x)
  result.add_edge(x[0], x[1], weight = cost)

pos = nx.spring_layout(result, seed=7)

plt.subplot(1,2,1)
nx.draw_networkx_nodes(nxgraph, pos, node_size=300)
nx.draw_networkx_labels(nxgraph, pos, font_size=10, font_family="sans-serif")
nx.draw_networkx_edges(
    nxgraph, pos, width=4, alpha=0.2, edge_color="b", style="dashed"
)
edge_labels = nx.get_edge_attributes(nxgraph, "weight")
nx.draw_networkx_edge_labels(nxgraph, pos, edge_labels)


plt.subplot(1,2,2)
nx.draw_networkx_nodes(result, pos, node_size=300)
nx.draw_networkx_labels(result, pos, font_size=10, font_family="sans-serif")
nx.draw_networkx_edges(
    result, pos, width=5, alpha=1.0, edge_color="r", style="solid"
)
edge_labels = nx.get_edge_attributes(result, "weight")
nx.draw_networkx_edge_labels(result, pos, edge_labels)




plt.show()

