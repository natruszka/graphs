import prj3_zad1 as prj
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

MyGraph = prj.RGraph()
MyGraph.randomize()

vertices_not_ready = sorted(MyGraph.vertices.copy())
vertice_processed = vertices_not_ready.pop(0)
vertices_ready = []

edges_not_ready = MyGraph.edges.copy()
edges_processed = []
edges_ready = []

def is_neighbour(vertice_1, vertice_2, edges):
    for edge in edges:
        if((edge[0] == vertice_1) and (edge[1] == vertice_2) 
        or (edge[1] == vertice_1) and (edge[0] == vertice_2)):
            return edge
    else:
        return None

def relax(u, v, w):
    if v[1] > u[1] + w:
        v[1] = u[1] + w
        v[2] = u[0]
    return v
    
def qompare(done_list, all_vertices):
    return len(done_list) == len(all_vertices)

def Dijkstra(graph, vertex=0):

    vertices_not_ready = sorted(graph.vertices.copy())
    vertice_processed = vertex
    vertices_ready = []

    edges_not_ready = graph.edges.copy()
    edges_processed = []
    edges_ready = []

    ds = [np.inf for _ in range(len(graph.vertices))]
    ps = [np.nan for _ in range(len(graph.vertices))]
    ds[0] = 0

    queue = [[vertice, np.inf, np.nan] for vertice in graph.vertices]
    queue[vertex][1] = 0                                                
    done = []    

    Draw(MyGraph, vertices_not_ready, vertice_processed, vertices_ready, edges_not_ready, edges_processed, edges_ready, ds, ps)                                                      

    while (not qompare(done, graph.vertices)):

        # correcting edges_ready
        for edge in edges_processed:
            edges_ready.append(edge)
        edges_processed = []

        min_ = queue[0]
        for item in queue:
            min_ = item if item[1] < min_[1] else min_
        
        
        # correcting vertices_ready and vertice_processed
        vertices_ready.append(vertice_processed)
        vertice_processed = min_[0]

        # correcting edges_processed
        for edge in edges_not_ready:
            if (edge[0] == vertice_processed or edge[1] == vertice_processed):
                edges_processed.append(edge)

        done.append(queue.pop(queue.index(min_)))

        for i in range(len(queue)):
            item = queue[i]
            tmp = is_neighbour(min_[0], item[0], graph.edges)
            if(tmp):
                queue[i] = relax(min_, item, tmp[2])

        Draw(MyGraph, vertices_not_ready, vertice_processed, vertices_ready, edges_not_ready, edges_processed, edges_ready, ds, ps)

    return done

def Undijkstrify(done, start):
    paths = []
    for i in range(len(done)):
        path = []
        prev = i + 1
        while prev != start:
            for item in done:
                prev = item[2] if item[0] == prev else prev
            path.insert(0, prev)
        paths.append(path)
    return paths

def Draw(graph,
        vertices_not_ready, vertice_processed, vertices_ready,
        edges_not_ready, edges_processed, edges_ready,
        ds, ps):

    # Drawing part

    vertice_colours = ["red" if vertice == vertice_processed else ("green" if vertice in vertices_ready else "blue") for vertice in graph.vertices]
    edge_colours = ["black" if edge in edges_ready else ("green" if edge in edges_processed else "grey") for edge in graph.edges]
    G_edges = [(edge[0], edge[1]) for edge in graph.edges]

    G = graph.to_nxGraph()
    pos = nx.shell_layout(G)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_color=vertice_colours, node_size=1200)
    # edges
    nx.draw_networkx_edges(G, pos, edgelist=G_edges, edge_color=edge_colours, width=3)
    # node labels
    node_labels = {}
    for i in range(len(graph.vertices)):
        node_labels[i+1] = "%d \n%.0f/%.0f" % (graph.vertices[i], ds[i], ps[i])
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    #ax = plt.gca()
    #ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    plt.show()



if __name__ == "__main__":
    MyGraph = prj.RGraph()
    MyGraph.randomize(vertice_count=7, edges_count=12)

    #Draw(MyGraph, vertices_not_ready, vertice_processed, vertices_ready, edges_not_ready, edges_processed, edges_ready, ds, ps)

    done = Dijkstra(MyGraph)
    print(done)
