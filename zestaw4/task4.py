import networkx as nx
import task3
import task1
import copy

def johnson(graph: nx.DiGraph):
    new_graph = add_s(graph)
    dist = task3.bellman_ford(new_graph, 's')
    if new_graph is None:
        raise "Graf zawiera cykl o ujemnej wadze"
    else:
        new_weights = {}
        for u, v, data in graph.edges(data=True):
            new_weights[(u, v)] = data['weight'] + dist[u] - dist[v]
        
        reweighted_graph = nx.DiGraph()
        for u, v in graph.edges:
            reweighted_graph.add_edge(u, v, weight=new_weights[(u, v)])

        new_graph.remove_node('s')

        distance_matrix = {node: {node: float('inf') for node in graph.nodes} for node in graph.nodes}

        for u in graph.nodes:
            distances, _ = nx.single_source_dijkstra(reweighted_graph, u)
            for v in distances:
                distance_matrix[u][v] = distances[v] - dist[u] + dist[v] 
    
    return distance_matrix

def add_s(graph:nx.DiGraph):
    new_graph = copy.deepcopy(graph)
    new_graph.add_node('s')
    for node in new_graph.nodes:
        if node != 's':
            new_graph.add_edge('s', node, weight=0)
    return new_graph

if __name__ == "__main__":
    graph = task1.random_digraph(10, 0.3)
    graph = task3.weighted_digraph_from_random_digraph(graph)
    try:
        dist_matrix = johnson(graph)
        task3.print_dict(dist_matrix)
        task3.draw_graph(graph)
    except:
        print("Graf zawiera cykl o ujemnej wadze")
            