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

def find_largest_component(graph: nx.Graph):
    components = ""
    i = 1
    all_components = init_DFS(graph, [])
    for component in all_components:
        components=components + str(i) +" "
        components= components + str(component) +"\n"
        i+=1
    components+="Największa spójna składowa: " + str(all_components.index(max(all_components, key=len))+1)
    return components

