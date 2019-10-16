import graph_util as gutil
import files
import numpy
import json

def main():

    station1 = 'ZAP28'
    station2 = 'RE16'

    get_shortest_path_dist_from_stat(station1, station2)
    #graph_dic, graph_edges = get_test_graph()
    #dijkstra(graph_dic, "0", graph_edges)
    #print(graph_dic)

def initialize():
    # Get road network
    graph_dic = gutil.get_graph(files.roads_pads_network_utm_geojson,
            files.roads_correction_utm_csv)

    # Get station info
    stat_id_dic = gutil.create_station_status_dic(files.station_status_utm_geojson,
            files.closest_to_road_geojson_utm )
    #print('stations count', len(station_dic))
    #print(station_dic)

    # Add mapping to station info dictionary
    road_not_found_stat = add_station_to_road_mapping(station_dic, graph_dic)
    #print(len(road_not_found_stat), 'stations cannot find road mapping')

    # Get station name to id mapping
    stat_name_dic = create_stat_name_id_mapping(station_dic)

    # [Debug] Find the closest road of station that fail mapping
    #closest_road_list = gutil.find_closest_road(road_not_found_stat,
    #        station_dic, graph_dic)

    sp_dic = {}
    stations = list(stat_id_dic)
    for i in range(len(stations)):
        for j in range(len(stations)):
            if i == j:
                continue
            id1 = stations[i]
            id2 = stations[j]
            stat_name1 = stat_name_dic[id1]
            stat_name2 = stat_name_dic[id2]
            path, dist = get_shortest_path_from_stat_id(id1, id2, stat_id_dic, graph_dic)
            key = stat_name1 + '#' + stat_name2
            dist_dic[key] = {}
            dist_dic[key]['distance'] = dist
            dist_dic[key]['path'] = path

    return graph_dic, station_id_dic, sp_dic

def get_shortest_path_dist_from_stat(stat1, stat2, sp_dic):
    key = stat1 + '#' + stat2
    if key not in sp_dic:
        print('Stations cannot be found')
        return -1

    return sp_dic[key]['distance'], sp_dic['path']

def create_stat_name_id_mapping(station_dic):
    stat_name_dic = {}
    for stat_id in station_dic:
        stat_name = station_dic[stat_id]['name']
        stat_name_dic[stat_name] = stat_id
    return stat_name_dic

def get_shortest_path_from_stat_id(src_id, dst_id, station_dic, graph_dic):
    if src_id not in station_dic or dst_id not in station_dic:
        print('Invalid station id')
        return
    road1_id = station_dic[src_id]['road_id']
    road2_id = station_dic[dst_id]['road_id']
    return get_shortest_path(road1_id, road2_id, graph_dic)

def add_station_to_road_mapping(station_dic, road_dic):
    road_not_found_stat = []
    for stat in station_dic:
        coordinate = station_dic.get(stat)['road_coordinates']
        station_dic.get(stat)['road_id'] = -1
        found = False
        for road_vertex in road_dic:
            road_coordinates = road_dic[road_vertex]['coordinates']
            if (int(coordinate[0]) == road_coordinates[0]
                    and int(coordinate[1]) == road_coordinates[1]):
                station_dic.get(stat)['road_id'] = road_vertex
                found = True
                break
        if not found and not (coordinate[0] == -1 and coordinate[1] == -1):
            print('Station', station_dic[stat]['name'], 'road mapping not found')
            road_not_found_stat.append(stat)
    return road_not_found_stat

def get_shortest_path(src, dst, graph_dic):
    dijkstra(src, graph_dic)
    path = get_dijkstra_path(src, dst, graph_dic)
    dist = get_dist_from_path(path, graph_dic)
    #print(path, dist)
    return path, dist

def get_dist_from_path(path, graph_dic):
    total = 0
    for vertex in path:
        if vertex not in graph_dic:
            return -1
        else:
            total += graph_dic.get(vertex)['dist']
    return total

def get_dijkstra_path(src, dst, graph_dic):
    if src  not in graph_dic or dst not in graph_dic:
        print(src, 'or', dst, 'not found in graph_dic')
        return
    path = []
    prev = dst
    while prev is not -1:
        path.insert(0, prev)
        prev = graph_dic.get(prev)['prev']
    
    #print(path)
    return path

def dijkstra(src, graph_dic):
#def dijkstra(graph_dic, src, graph_edges):
    if src not in graph_dic:
        print("src " + str(src) + " not in roads network")
        return
    vertices = set(graph_dic.keys())
    for vertex_id in graph_dic:
        graph_dic.get(vertex_id)['dist'] = numpy.Inf
        graph_dic.get(vertex_id)['prev'] = -1
    graph_dic.get(src)['dist'] = 0

    while vertices:
        min_dist_vertex, min_dist = get_min_dist(graph_dic, vertices)
        #print('*** ', min_dist_vertex, min_dist, '***')
        vertices.remove(min_dist_vertex)
        
        for neighbor in graph_dic.get(min_dist_vertex)['adj']:
            if neighbor in vertices:
                old_dist = graph_dic.get(neighbor)['dist']
                new_dist = (graph_dic.get(min_dist_vertex)['dist'] + 
                    gutil.get_dst_from_vertex_id(min_dist_vertex, neighbor, graph_dic))
                #+ get_test_dist(min_dist_vertex, neighbor, graph_edges)
                #print('old_dist', old_dist, 'new dist',new_dist)
                if new_dist < old_dist:
                    #print('update', neighbor)
                    graph_dic.get(neighbor)['dist'] = new_dist
                    graph_dic.get(neighbor)['prev'] = min_dist_vertex

def get_min_dist(graph_dic, vertex_set):
    min_dist_vertex = -1
    min_dist = numpy.Inf
    for vertex in vertex_set:
        if graph_dic.get(vertex)['dist'] < min_dist:
            min_dist_vertex = vertex
            min_dist = graph_dic.get(vertex)['dist']
    return min_dist_vertex, min_dist

def get_test_graph():
    graph_dic = {}
    graph_edges = {}
    
    with open(files.tmp_adj_json) as json_file:
        graph_dic = json.load(json_file)
    
    with open(files.tmp_dist_json) as json_file:
        graph_edges = json.load(json_file)

    #print(graph_dic)
    #print(graph_edges)
    return graph_dic, graph_edges

def get_test_dst(v1, v2, graph_edges):
    if v1 > v2:
        tmp = v1
        v1 = v2
        v2 = tmp
    key = str(v1) + '#' + str(v2)
    if key in graph_edges:
        return graph_edges.get(key)
    print("edge:" + key + " not found")


if __name__ == '__main__':
    main()
