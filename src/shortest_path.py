import math
import files
from collections import defaultdict, deque
from graph_util import get_graph


def main():
    
    graph_dic = get_graph(files.roads_pads_network_utm_geojson,
            files.roads_correction_utm_csv)

    graph = Graph()

    for node in graph_dic.keys():
        graph.add_node(node)

    for from_node in graph_dic.keys():
        for to_node in graph_dic[from_node]['adj']:
            if (to_node > from_node):
                dist = euclidean(graph_dic[from_node]['easting'], 
                        graph_dic[from_node]['northing'],
                        graph_dic[to_node]['easting'], 
                        graph_dic[to_node]['northing'])
                graph.add_edge(from_node, to_node, dist)

    print(graph)

    # shortest distance, path
    print(shortest_path(graph, 3578, 3587))


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        
    def __str__(self):   
        return "Graph: {0} nodes, {1} edges\n".format(
                len(self.nodes), len(self.edges)) \
                + "Nodes:\n{0}\nEdges:\n{1}\nDistances:\n{2}".format(
                self.nodes, self.edges, self.distances)

def shortest_path(graph, origin, destination):
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)


def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def euclidean(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


if __name__ == '__main__':
    main()
