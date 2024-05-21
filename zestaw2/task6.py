import task1and2 as t12
import task3 as t3
import networkx as nx
import matplotlib.pyplot as plt  
import random  
import z5 as t5
import numpy as np


def is_hamiltonian(graph: nx.Graph):
    
    if (nx.is_connected(graph)): #czy spójny?
        for node in graph.nodes: #kompletny brute force, wybaczcie, bez tej linijki czasem nie odnajduje
            stack = t3.DFS(graph, node, [], [])
            print(stack)
            if len(stack) == len(graph.nodes): #wystarczy sprawdzic dlugosc listy wierzcholkow, bo cykl Hamiltona wlasnie zaklada wszystkie wierzchołki
                if graph.has_edge(stack[-1], stack[0]): #kluczowy punkt
                    stack.append(stack[0])
                    print('Cykl Hamiltona: ' + str(stack))
                    return stack
        print('Nie odnaleziono cyklu Hamiltona.')
        return None
    else:
        print('Graf musi być spójny!')
        return None
    

# G = nx.Graph()
# G.add_edge(1,3)
# G.add_edge(1,6)
# G.add_edge(2,4)
# G.add_edge(2,6)
# G.add_edge(4,5)
# G.add_edge(5,1)
# G.add_edge(5,2)
# G.add_edge(5,3)

G = nx.Graph()
# G.add_edge(1,2)
# G.add_edge(1,5)
# G.add_edge(1,7)
# G.add_edge(1,10)
# G.add_edge(2,3)
# G.add_edge(2,6)
# G.add_edge(2,8)
# G.add_edge(3,4)
# G.add_edge(3,7)
# G.add_edge(3,9)
# G.add_edge(4,5)
# G.add_edge(4,8)
# G.add_edge(4,10)
# G.add_edge(5,6)
# G.add_edge(5,9)
# G.add_edge(6,11)
# G.add_edge(7,11)
# G.add_edge(10,11)
# G.add_edge(9,11)
# G.add_edge(8,11)


# G = t12.create_graph_from_sequence([4,4,4,4,4,3,3,3,3,3,5])

# print(is_hamiltonian(G))
# nx.draw_circular(G,with_labels=True)
# plt.show()
# graph2 = t5.generate_random_regular_graph(6, 2)
# print(is_hamiltonian(graph2))
# nx.draw_circular(graph2,with_labels=True)
# plt.show()


graph3 = t5.generate_random_regular_graph(10, 5) #generowanie grafu z zadania 5
print(is_hamiltonian(graph3))
nx.draw_circular(graph3,with_labels=True)
plt.show()

    