# Autorka: Aleksandra Michalska

# Używając powyższych programów, napisać program do tworzenia losowego grafu
# eulerowskiego i znajdowania na nim cyklu Eulera.
import task1and2 as t12
import task3 as t3
import networkx as nx
import matplotlib.pyplot as plt    

def can_be_euler_graph(graph: nx.Graph): #check for even nodes and component
    if any(degree[1]%2 for degree in graph.degree()): #check if any node degree is odd
        return False #every node should have even degree
    if len(t3.init_DFS(graph, [])) > 1:
        return False
    return True

def find_euler_cycle(graph: nx.Graph, u: int, cycle: list):
    v_nodes = [v for v in graph.neighbors(u)]
    for v in v_nodes:
        if can_remove_edge(graph, u, v):
            cycle.append((u,v))
            graph.remove_edge(u, v)
            # nx.draw(graph, with_labels = True)
            # plt.show()
            cycle = find_euler_cycle(graph, v, cycle)
    return cycle
    

def can_remove_edge(graph: nx.Graph, u, v):
    if len([n for n in graph.neighbors(u)]) == 1:
        return True
    if(not graph.has_edge(u,v)):
        return False
    reachable_nodes_before_removing = t3.DFS(graph, u ,[],[])
    graph.remove_edge(u,v)
    reachable_nodes_after_removing = t3.DFS(graph, u, [], [])
    graph.add_edge(u,v)
    return len(reachable_nodes_before_removing) <= len(reachable_nodes_after_removing)

graph = t12.create_graph_from_sequence([4, 4, 4, 4, 4, 2, 2])
# nx.draw(graph, with_labels = True)
# plt.show()
print(can_be_euler_graph(graph))
print(find_euler_cycle(graph,1, []))