import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import igraph as ig
import numpy as np

class RGraph():
    def __init__(self, vertices=[], edges=[]):
        self.vertices = vertices
        self.edges = edges

    def edge_exists(self, edge):
        for own_edge in self.edges:
            if own_edge[0] == edge[0] and own_edge[1] == edge[1]: return True
            if own_edge[1] == edge[0] and own_edge[0] == edge[1]: return True
        return False

    def vertice_has_edge(self, vertice):
        for edge in self.edges:
            if edge[0] == vertice or edge[1] == vertice: return True
        return False
    
    def randomize(self, vertice_count=12, edges_count=20, edgeweight_start=1, edgeweight_end=10):
        self.vertices = list(range(1, vertice_count+1))
        self.edges = []
        while len(self.edges) < edges_count:
            edge = [randint(1, vertice_count), randint(1, vertice_count), randint(edgeweight_start, edgeweight_end)]
            if( edge[1] == edge[0] or self.edge_exists(edge)): continue     # eliminacja pętli lub powtórzenia
            self.edges.append(edge)

        for vertice in self.vertices:
            if(not self.vertice_has_edge(vertice)):
                for i in range(randint(0, 4)):
                    edge = [vertice, randint(1, vertice_count), randint(edgeweight_start, edgeweight_end)]
                    if( edge[1] == edge[0] or self.edge_exists(edge)): continue     # eliminacja pętli lub powtórzenia
                    self.edges.append(edge)

            if(not self.vertice_has_edge(vertice)):
                if vertice == 1:
                    self.edges.append([vertice, 2, randint(edgeweight_start, edgeweight_end)])
                else:
                    self.edges.append([vertice, 1, randint(edgeweight_start, edgeweight_end)])

    def get_edges(self):
        #edges = list(map(sorted, self.edges.copy()))
        return self.edges

    def get_vertices(self):
        return self.vertices

    def get_edges_as_matrix(self):
        edgemat = np.zeros((len(self.vertices), len(self.vertices)))
        for edge in self.edges:
            edgemat[edge[0]-1][edge[1]-1] = edge[2]
            edgemat[edge[1]-1][edge[0]-1] = edge[2]
        return edgemat

    def to_nxGraph(self):
        G = nx.Graph()
        G.add_nodes_from(self.vertices)
        for edge in self.edges:
            G.add_edge(edge[0], edge[1], weight=edge[2])
        return G

    def draw(self):
        G = self.to_nxGraph()
        pos = nx.shell_layout(G)

        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=800)
        # edges
        nx.draw_networkx_edges(G, pos, width=1)
        # node labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
        # edge weight labels
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)

        #ax = plt.gca()
        #ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

        # source: https://networkx.org/documentation/stable/auto_examples/drawing/plot_weighted_graph.html


    def to_igraph(self):
        weights = []

        G = ig.Graph()
        G.add_vertices(len(self.vertices))
        for edge in self.edges:
            print(edge)
            G.add_edge(edge[0]-1, edge[1]-1)
            weights.append(edge[2])

        G.vs["num"] = self.vertices
        G.es["weight"] = weights
        G.es['label'] = weights

        return G

    # Działa ale jest brzydkie, proszę korzystać z draw()
    def paint(self):
        g = self.to_igraph()

        fig, ax = plt.subplots(figsize=(5,5))
        ig.plot(
            g,
            target=ax,
            layout="circle", # print nodes in a circular layout
            vertex_size=30,
            #vertex_color=["steelblue" if gender == "M" else "salmon" for gender in g.vs["gender"]],
            vertex_frame_width=4.0,
            vertex_frame_color="white",
            vertex_label=g.vs["num"],
            vertex_label_size=7.0,
            #edge_width=[2 if married else 1 for married in g.es["married"]],
            #edge_color=["#7142cf" if married else "#AAA" for married in g.es["married"]]
            edge_labels=g.es["weight"]
        )

        plt.show()

        # source: https://python.igraph.org/en/stable/tutorials/quickstart.html

if __name__ == '__main__':
    MyGraph = RGraph()
    MyGraph.randomize()

    print(MyGraph.get_edges())
    print(MyGraph.get_vertices())
    print(MyGraph.get_edges_as_matrix())

    MyGraph.draw()