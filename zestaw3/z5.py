'''
graph = [
  [0,0,5,1],
  [0,0,4,6],
  [5,4,0,10],
  [1,6,10,0]
]'''

graph = [
  [0,0,5,1,7],
  [0,0,4,6,2],
  [5,4,0,10,0],
  [1,6,10,0,0],
  [7,2,0,0,0]
]

elem = range(len(graph))
edges = []

for i in range(len(graph)):
  for j in range(i):
    if graph[i][j] > 0:
      edges.append((set((i+1,j+1)),graph[i][j]) )


tree_set = [{i+1} for i in range(len(graph))]
edge_set = []


for i in range(len(graph)-1):
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
  print(edge_set)
  print(tree_set)
  print()
  
print(edge_set)
print(tree_set)










