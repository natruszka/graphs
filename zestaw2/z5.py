import networkx as nx
import numpy as np
import sys
import random as rng
import matplotlib.pyplot as plt


# {arg1} {arg2}
# arg1 = ilosc wierzcholkow
# arg2 = stopien kazdego

def generate_random_regular_graph(n: int, k: int):

    # kontrola wejscia
    if k % 2:
        if n % 2:
            raise ValueError("Jesli stopien nieparzysty to ilosc parzysta")

    if k >= n:
        raise ValueError("Przepelnienie grafu")


    vert = [{"index" : i, "deg" : k} for i in range( n)]
    edge = set()



    for iter in range((k*n) //2):
        vert.sort(key= lambda x:  (x["deg"],np.random.randint(0,1+x["deg"])),reverse=True ) #sortuje po stopniu
        #print(vert)

        #iteruje po max_deg nastepnych w tablece
        #1|2|3|4
        #-------
        #3|2|2|1
        #  ^ ^ ^
        #-1 -1 -1
        max_deg = vert[0]["deg"]
        for i in range(max_deg):
            new_edge = (vert[0], vert[i+1])

            vert[i+1]["deg"] -=1 #redukuje stopien
            edge.add( (new_edge[0]["index"], new_edge[1]["index"] ))

        for i in vert[1:max_deg+1]: #sprawdzam czy po redukcji mozna usunac zuzyte wiezholki
            if i["deg"] <= 0:
                vert.remove(i)

        vert.pop(0) #usuwam zuzyty wiezholek z poczatku
        if len(vert) == 0:
            break



    for randiter in range(0,  (k*n) // 2 ):
        old_pair = rng.sample(list(edge),2)
        old_pair_as_set = list(map(set,old_pair))
        if old_pair_as_set[0].isdisjoint(old_pair_as_set[1]): #krawedzie nie maja wspolnego wiezholka
            swapped = [ (old_pair[0][0], old_pair[1][0] ),(old_pair[0][1], old_pair[1][1] )  ]
            swapped_as_set = [set(swapped[0]), set(swapped[1])]
            print(swapped_as_set[0],swapped_as_set[1])

            for elem in map(set,edge): #zabezpieczam przed podwojna krawedzia
                if elem.issubset(swapped_as_set[0]) or elem.issubset(swapped_as_set[1]):
                    
                    break
            else: #nie ma kolizji, mozna dodac
                for elem in old_pair:
                    edge.remove(elem)
                for elem in swapped:
                    edge.add(elem)



    graph = None
    if(k > 0):
        graph = nx.from_edgelist(edge)
    elif n > 0:
        graph = nx.Graph()
        graph.add_nodes_from(range(0,n))
    else:
        graph = nx.Graph()

    return graph 
    
if __name__ == '__main__':
	nx.draw_circular(generate_random_regular_graph(10,3))
	plt.show()





