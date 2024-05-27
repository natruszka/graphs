"""Graf_zestaw5.py
Zadanie 1: Napisać program do tworzenia losowej sieci przepływowej między pojedynczym źródłem i pojedynczym ujściem.
"""


import random
import networkx as nx
import matplotlib.pyplot as plt


def create_random_flow_network(N):
    if N < 2:
      print('nie.')
      return
    #Tworzenie warstw i wierzchołków
    #Jak więcej warstw niż 5, to boję się o stan alfabetu...
    if N > 5:
      k = 1
    else:
      k = 'a'
    layers = [[] for _ in range(N + 2)]
    layers[0].append("s")
    layers[N + 1].append("t")

    for i in range(1, N + 1):
        num_vertices = random.randint(2, N)
        for j in range(num_vertices):
            if k == 's':
              k = chr(ord(k) + 2)
            elif k == 't':
              k = chr(ord(k) + 1)
            layers[i].append(f"{k}")
            if N <= 5:
              k = chr(ord(k) + 1)
            else:
              k += 1

    #Tworzenie grafu
    G = nx.DiGraph()

    #Dodawanie wierzchołków
    for i, layer in enumerate(layers):
        for v in layer:
            G.add_node(v)
            G.nodes[v]['subset'] = i #Przypisanie klucza subset do numeru danej warstwy

    #Łączenie wierzchołków między warstwami
    for i in range(N + 1):
        for u in layers[i]:
            next_layer = layers[i + 1]
            num_edges = random.randint(1, len(next_layer))
            if i == 0 or i == N:
              next_v = next_layer
            else:
              next_v = random.sample(next_layer, num_edges)
            for v in next_v:
                G.add_edge(u, v, capacity=random.randint(1, 10), flow=0) #losowa przepustowość i zerowy przepływ

    #Dodawanie dodatkowych 2N losowych łuków
    all_vertices = [v for layer in layers for v in layer if v not in ["s", "t"]]
    additional_edges = 2 * N
    #Losowy wybór
    while additional_edges > 0:
        u = random.choice(all_vertices)
        v = random.choice(all_vertices)
        if u != v and not G.has_edge(u, v):
            G.add_edge(u, v, capacity=random.randint(1, 10), flow=0)
            additional_edges -= 1
    #layers jest istotne dla algorytmu niżej, bo jest używane przy tworzeniu grafu sieci rezydualnej Gf
    return G, layers

def draw_flow_network(G, N):
    plt.figure(figsize=(2*N**1.5,N**1.5)) #(uwaga, upewnić się że mamy zasoby, by wyliczać obrazki wieksze niz N = 20)
    pos = nx.multipartite_layout(G, subset_key='subset') #Stwarza warstwy jako pionowe linie według klucza 'subset'
    edge_labels = nx.get_edge_attributes(G, 'capacity') #Wszystkie wartości krawędzi capacity -> czyli przepustowości
    nx.draw(G, pos, with_labels=True, node_size=500, arrows=True)
    d = nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', label_pos=0.7) #0.7, czyli informacja o przepustowości znajduje się bliżej wierzchołka DOCELOWEGO niż źródłowego -> by zapobiec nadpisywaniu się wartości
    plt.savefig("Graf_G_wejście")

#Parametr N
N = 3 #Można zmienić wartość N dla testowania

# Tworzenie i rysowanie sieci przepływowej
G, layers = create_random_flow_network(N)
draw_flow_network(G,N)
plt.show()
'''
Zadanie 2:

Zastosować algorytm Forda-Fulkersona do znalezienia maksymalnego przepływu na sieci z zadania pierwszego. 
Ścieżki powiększające wybierać jako ścieżki o najmniejszej liczbie krawędzi. 
Do ich wyszukiwania użyć przeszukiwania wszerz.
'''

from collections import deque
from networkx.algorithms.flow.utils import build_residual_network

def reconstruct_path(ps, start, end):
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = ps[current]

    #Odwrócenie ścieżki, ponieważ była konstruowana od końca do początku
    path.reverse()

    #Sprawdzenie, czy ścieżka rzeczywiście zaczyna się od 'startu'
    if path[0] == start:
        return path
    else:
        return None  #Brak ścieżki z start do end


def bfs(G, s):
    #Inicjalizacja: przypisanie wszystkim wierzchołkom odległości nieskończonej (tu: float('inf'))
    ds = {node: float('inf') for node in G.nodes()}
    ps = {node: None for node in G.nodes()}

    #Odległość od źródła s do samego siebie wynosi 0
    ds[s] = 0

    #Utworzenie pustej kolejki
    Q = deque([s])

    #Dopóki kolejka nie jest pusta
    while Q:
        #Ściągnięcie wierzchołka z początku kolejki
        v = Q.popleft()

        #Iteracja po sąsiadach wierzchołka v
        for u in G.neighbors(v):
            if ds[u] == float('inf'):  #Jeśli u nie był odwiedzony
                ds[u] = ds[v] + 1  # aktualizacja odległości
                ps[u] = v  #ustawienie poprzednika
                Q.append(u)  #dodanie wierzchołka u do kolejki
    #print (f'Odległości: {ds}, lista następstw: {ps}')
    return ds, ps

def isPathExisting(Gf): 
  ds, ps = bfs(Gf, 's') #ds to odległości wierzchołków, ps to najkrótsza ścieżka
  path = reconstruct_path(ps, 's', 't')
  return path

def removingIfZero(Gf):
  edge_labels = nx.get_edge_attributes(Gf, 'capacity')
  for key, value in list(edge_labels.items()):
      if value == 0:
          Gf.remove_edge(key[0], key[1])
          del edge_labels[key]

def ford_fulkerson(G, layers, N):
  nx.set_edge_attributes(G, 0, 'flow') #zeruje przepływy
  Gf = build_residual_network(G, 'capacity') #buduje residualną sieć na podstawie istniejącej sieci przepływów
  for i, layer in enumerate(layers):
          for v in layer:
            Gf.nodes[v]['subset'] = i #oznacza warstwy (przydatne do wyświetlania)
  removingIfZero(Gf) #gdyby powstała jakaś krawędź o zerowej przepustowości
  path = isPathExisting(Gf)
  while path is not None:
    cfp = min(Gf[u][v]['capacity'] for u, v in zip(path[:-1], path[1:])) #min (u,v) należących do ścieżki  
    #Aktualizacja przepływów w grafie G
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if G.has_edge(u, v):
            G[u][v]['flow'] += cfp
        else:
            G[v][u]['flow'] -= cfp

        #Aktualizowanie sieci rezydualnej
        if Gf.has_edge(u, v):
            Gf[u][v]['capacity'] -= cfp
            if Gf[u][v]['capacity'] == 0:
                Gf.remove_edge(u, v)
        #W obie strony...
        if not Gf.has_edge(v, u):
            Gf.add_edge(v, u, capacity=cfp)
        else:
            Gf[v][u]['capacity'] += cfp  
    path = isPathExisting(Gf) #Wyliczanie ścieżki
  #liczenie tak o 
  fmax = sum(G['s'][u]['flow'] for u in list(G.neighbors('s'))) #Wystarczy policzyć wierzchołki wychodzące ze źródła
  
  plt.figure(figsize=(2*N**1.5,N**1.5)) #(uwaga, upewnić się że mamy zasoby, by wyliczać obrazki wieksze niz N = 20)
  edge_labels = nx.get_edge_attributes(Gf, 'capacity') 
  pos = nx.multipartite_layout(Gf, subset_key='subset') #To ustawia nam pozycje sieci przepływowej według warstw
  nx.draw(Gf, pos, with_labels=True, node_size=500, arrows=True)
  #0.7, czyli informacja o przepustowości znajduje się bliżej wierzchołka DOCELOWEGO niż źródłowego -> by zapobiec nadpisywaniu się wartości
  nx.draw_networkx_edge_labels(Gf, pos, edge_labels=edge_labels, font_color='green', label_pos = 0.7)
  plt.savefig("Siec residualna")
  plt.figure(figsize=(2*N**1.5,N**1.5)) #(uwaga, upewnić się że mamy zasoby, by wyliczać obrazki wieksze niz N = 20)
  edge_labels = {edge: f"{data['flow']}/{data['capacity']}" for edge, data in G.edges.items()}
  pos = nx.multipartite_layout(G, subset_key='subset')
  nx.draw(G, pos, with_labels=True, node_size=500, arrows=True)
  dd = nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', label_pos = 0.7) 
  plt.savefig(f'Wyjscie_algorytmu,fmax = {fmax}')
  print(f'|fmax| = {fmax}')
  plt.show()


def algo(N):
  # Tworzenie i rysowanie sieci przepływowej
  G, layers = create_random_flow_network(N)
  draw_flow_network(G,N)
  #testowanie
  ford_fulkerson(G, layers, N)

#Można zmienić wartość N dla testowania
algo(5)