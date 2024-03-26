# Autorka: Aleksandra Michalska

# 1. Napisać program do sprawdzania, czy dana sekwencja liczb naturalnych
# jest ciągiem graficznym, i do konstruowania grafu prostego o stopniach
# wierzchołków zadanych przez ciąg graficzny.

import networkx as nx

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


print(check_if_degree_sequence([2,2,6,4,4,6,6]))
print(create_graph_from_sequence([1, 3, 2, 3, 2, 4, 1]))