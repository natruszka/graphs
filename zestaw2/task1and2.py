# Autorka: Aleksandra Michalska

# 1. Napisać program do sprawdzania, czy dana sekwencja liczb naturalnych
# jest ciągiem graficznym, i do konstruowania grafu prostego o stopniach
# wierzchołków zadanych przez ciąg graficzny.

import networkx as nx
import random
import matplotlib.pyplot as plt    

def check_if_degree_sequence(sequence: list) -> bool:
    #Sprawdzenie, czy suma stopni wierzchołków jest parzysta
    if sum(sequence)%2 != 0:
        return False
    
    sequence = sorted(sequence, reverse=True)
    n = len(sequence) #n - ilość wierzchołków

    while True:
        if all(seq == 0 for seq in sequence):
            return True
        if sequence[0] >= n or any(seq < 0 for seq in sequence):
            return False
        for i in range(1, sequence[0]+1):
            sequence[i] = sequence[i] - 1
        sequence[0] = 0
        sequence = sorted(sequence, reverse=True)

def create_graph_from_sequence(sequence: list) -> nx.Graph:
    if not check_if_degree_sequence(sequence):
        return None
    sequence = sorted(sequence, reverse=True)
    graph_list = list(map(list, zip(range(1, len(sequence)+1),sequence)))

    graph = nx.Graph()
    graph.add_nodes_from([n for n in range(1, len(sequence)+1)])
    graph_list = sorted(graph_list, key=lambda x: x[1], reverse=True)

    while True:
        if all(tpl[1] == 0 for tpl in graph_list):
            return graph
        for i in range(1, graph_list[0][1]+1):
            graph_list[i][1] = graph_list[i][1] - 1
            graph.add_edge(graph_list[0][0], graph_list[i][0])
        graph_list[0][1] = 0
        graph_list = sorted(graph_list, key=lambda x: x[1], reverse=True)

# 2. Napisać program do randomizacji grafów prostych o zadanych stopniach
# wierzchołków. Do tego celu wielokrotnie powtórzyć operację zamieniającą losowo
# wybraną parę krawędzi: (a, b) i (c, d) na parę (a, d) i (b, c).

def get_two_different_random_integers_in_range(len: int) -> tuple:
    first, second = random.randint(0,len-1), random.randint(0,len-1)
    while first is second:
        first, second = random.randint(0,len-1), random.randint(0,len-1)
    return (first, second)

def swap_nodes(first_edge, second_edge, list_edges):
    if (first_edge[0], second_edge[1]) in list_edges or (first_edge[1],second_edge[0]) in list_edges: #sprawdzenie krawdzi wielokrotnych
        return None, None
    if first_edge[0] == second_edge[1] or first_edge[1] == second_edge[0]: #sprawdzenie petli
        return None, None
    if first_edge[0] == second_edge[0]: #zapobiega nieznaczacym permutacjom
        return None, None
    return (first_edge[0],second_edge[1]),(first_edge[1],second_edge[0])

def randomize_edges(random_amount: int, sequence: list) -> nx.Graph:
    if not check_if_degree_sequence(sequence):
        return None
    graph = create_graph_from_sequence(sequence)
    for _ in range(random_amount):
        list_edges = list(graph.edges)
        # print(list_edges)
        first_edge_index, second_edge_index = get_two_different_random_integers_in_range(len(list_edges))
        first_edge, second_edge = list_edges[first_edge_index], list_edges[second_edge_index]
        # print(first_edge, second_edge)
        first_edge_new, second_edge_new = swap_nodes(first_edge, second_edge, list_edges)

        while(first_edge_new == None and second_edge_new == None):
            first_edge_index, second_edge_index = get_two_different_random_integers_in_range(len(list_edges))
            first_edge, second_edge = list_edges[first_edge_index], list_edges[second_edge_index]
            # print(first_edge, second_edge)
            first_edge_new, second_edge_new = swap_nodes(first_edge, second_edge, list_edges)
        graph.remove_edges_from((first_edge, second_edge))
        graph.add_edges_from((first_edge_new, second_edge_new))
    return graph
