import networkx as nx
import task1
import random
import matplotlib.pyplot as plt

def bellman_ford(Graph: nx.DiGraph, source):
    dist = {node: float("Inf") for node in Graph.nodes}
    predecessor = {node: None for node in Graph.nodes}
    dist[source] = 0
    for _ in range(len(Graph.nodes) -1):
        for u, v, data in Graph.edges(data=True):
            w = data['weight']
            #relaksacja:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                predecessor[v] = u

    for u, v, data in Graph.edges(data=True):
        weight = data['weight']
        if dist[v] > dist[u] + weight:
            print("Graph contains negative weight cycle")
            return None
    return dist

def distance_matrix_bellman_ford(Graph = nx.DiGraph):
    dist_matrix = {node: {node: float('Inf') for node in Graph.nodes} for node in Graph.nodes}
    for src in Graph.nodes:
        dist = bellman_ford(Graph, src)
        if dist:
            for end_node in Graph.nodes:
                dist_matrix[src][end_node] = dist[end_node]
    return dist_matrix
    

def draw_graph(graph: nx.DiGraph):
    plt.figure()    
    pos = nx.circular_layout(graph) #spectral_layout, spring_layout, 
    weight_labels = nx.get_edge_attributes(graph,'weight')
    nx.draw(graph,pos,font_color = 'white', with_labels = True,)
    nx.draw_networkx_edge_labels(graph,pos,edge_labels=weight_labels)
    plt.show()

def weighted_digraph_from_random_digraph(graph: nx.DiGraph):
    edges = [(u,v) for u,v in graph.edges]
    return nx.DiGraph((u, v, {'weight': random.randint(-5,10)}) for (u,v) in edges)

def print_dict(dist_matrix):
    dist_matrix = dict(sorted(dist_matrix.items()))
    for k,v in dist_matrix.items():
        print(k, ": ", dict(sorted(v.items())))

if __name__ == "__main__":
    graph = task1.random_digraph(5, 0.2)
    graph = weighted_digraph_from_random_digraph(graph)
    dist_matrix = distance_matrix_bellman_ford(graph)
    print_dict(dist_matrix)
    draw_graph(graph)