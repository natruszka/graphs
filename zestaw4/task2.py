import networkx as nx
import random
import task1


def dfs_visit(graph, node, visited, stack):
    visited.add(node)
    for neighbor in graph.neighbors(node):
        if neighbor not in visited:
            dfs_visit(graph, neighbor, visited, stack)
    stack.append(node)

def components_r(graph, node, visited, component):
    visited.add(node)
    component.append(node)
    for neighbor in graph.neighbors(node):
        if neighbor not in visited:
            components_r(graph, neighbor, visited, component)

def kosaraju(graph):
    stack = []
    visited = set() #set, poniewaz nie pozwala na duplikaty

    for node in graph.nodes:
        if node not in visited:
            dfs_visit(graph, node, visited, stack)

    reversed_graph = graph.reverse()

    visited.clear()
    scc = []
    while stack:
        node = stack.pop()
        if node not in visited:
            component = []
            components_r(reversed_graph, node, visited, component)
            scc.append(component)
    return scc


digraph = task1.random_digraph(10, 0.2)
scc = kosaraju(digraph)
print("Silnie spójne składowe:", scc)