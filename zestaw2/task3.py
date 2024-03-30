# Autorka: Aleksandra Michalska

# Napisać program do znajdowania największej spójnej składowej na grafie.

import task1and2 as t12
import networkx as nx

def DFS(graph: nx.Graph, node: int, visited: list, nodes_in_component: list):
    if node not in visited:
        visited.append(node)
        nodes_in_component.append(node)
        for neighbor in graph.neighbors(node):
            nodes_in_component = DFS(graph, neighbor, visited, nodes_in_component) 
    return nodes_in_component

def init_DFS(graph: nx.Graph, visited: list):
    visited = []
    all_components = []
    for node in graph.nodes():
        component = []
        all_components.append(DFS(graph, node, visited, component))
    return [component for component in all_components if component] #remove empty components

# all_components = init_DFS(t12.create_graph_from_sequence([1, 3, 2, 3, 2, 4, 1]), [])
# print(all_components)

# all_components = init_DFS(t12.create_graph_from_sequence([4, 4, 4, 4, 4, 2, 2]), [])
# print(all_components)