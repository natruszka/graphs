# ZADANIE 3
# Napisać program do generowania grafów losowych G(n, l) oraz G(n, p).
# Źródło algorytmu: https://d-nb.info/1097267016/34
# Autor: Arkadiusz Rudy

import networkx as nx
import random as rng
import itertools
import numpy as np
import matplotlib.pyplot as plt
import time


def G_n(n,l):
#n - liczba wierzcholkow
#l - liczba krawedzi
  if l < 1 or (n*(n-1))//2 < l:
    raise ValueError

  G = nx.Graph()
  G.add_nodes_from(range(n))

  E = set()

  while len(E) < l:
    p = rng.randint(1,n-1)
    q = rng.randint(0,p-1) 
    E.add((q,p))
  G.add_edges_from(E)
  return G

def G_p(n, p):
  def G_p_dense(n,p):
  #n - liczba wiezholkow
  #p - prawdopodobienstwo, ze krawedz k bedzie wybrana
    G = nx.Graph()
    G.add_nodes_from(range(n))

    E = {k for k in itertools.combinations(range(n),r=2) if np.random.rand() < p }
    G.add_edges_from(E)
    return G

  def G_p_sparse(n,p):
  #n - liczba wiezholkow
  #p - prawdopodobienstwo, ze krawedz k bedzie wybrana
    G = nx.Graph()
    G.add_nodes_from(range(n))
    v = 1
    w = -1
    while True:
      w+= 1 + np.floor(np.log(1 - np.random.rand()) / np.log(1 - p))
      while v <= w and v < n:
        w-=v
        v+=1
      if v < n:
        G.add_edge(v,w)
      else:
        break

    return G
  if p == 0:
    return None
  if 0.1 < p:
    return G_p_sparse(n,p)
  else:
    return G_p_dense(n,p)




#print(G_n(1000000,500000))
#start = time.process_time()
#print(G_p(10000,0.10))
#print(time.process_time() - start)


plt.subplot(1,2,1)
nx.draw_circular(G_n(11,54))
plt.subplot(1,2,2)
nx.draw_circular(G_p(11,1))
plt.show()
