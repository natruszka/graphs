import networkx as nx
import random
import matplotlib.pyplot as plt

def print_matrix(matrix):
    for line in matrix:
        print(line)

def random_digraph(nodes: int, probability: float)->nx.Graph:
    if probability > 1 or probability < 0:
        raise ValueError("Prawdopodobieństwo nie może być mniejsze od 0 lub większe od 1.")
    if nodes < 1 or nodes > 50:
        raise ValueError("Ilość wierzchołków musi być większa od 0 lub mniejsza niz 50.")
    graph = nx.DiGraph()
    graph.add_nodes_from(range(1, nodes+1))
    for node in graph.nodes:
        for sec_node in graph.nodes:
            if node == sec_node:
                continue
            add_edge = random.random() < probability
            if add_edge:
                if (node, sec_node) in graph.edges:
                    continue
                graph.add_edge(node, sec_node)
    return graph

def graph_to_adjency_list(graph: nx.DiGraph):
    adj_list = {}
    for node in graph:
        adj_list[node] = []
        for neighbor in graph.neighbors(node):
            adj_list[node].append(neighbor)
    return adj_list

def graph_to_adjency_matrix(graph: nx.DiGraph):
    adj_matrix = [[0 for _ in graph.nodes] for _ in graph.nodes]
    for node in graph:
        for neighbor in graph.neighbors(node):
            adj_matrix[node-1][neighbor-1] = 1    
    return adj_matrix

def graph_to_incidence_matrix(graph: nx.DiGraph):
    incidence_matrix = [[0 for _ in graph.edges] for _ in graph.nodes]
    edges = [e for e in graph.edges]
    for i in range(len(graph.edges)):
        incidence_matrix[edges[i][0]-1][i] = 1
        incidence_matrix[edges[i][1]-1][i] = -1
        
    return incidence_matrix


if __name__ == "__main__":
    graph = random_digraph(5, 1)
    print(graph_to_adjency_list(graph))
    print_matrix(graph_to_adjency_matrix(graph))
    print_matrix(graph_to_incidence_matrix(graph))
    nx.draw_circular(graph, with_labels = True, font_color="whitesmoke")
    plt.show()