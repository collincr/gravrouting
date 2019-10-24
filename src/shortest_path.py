import graph_util as gutil
import files
import numpy
import json
import csv
import os.path

def main():

    preprocess()
    #get_not_ready_station()
    #get_all_stations_spt()
    #get_all_stations_spt_dic_from_file()

    #internal_get_spt_from_stat_name()

    #graph_dic, graph_edges = get_test_graph()
    #dijkstra(graph_dic, "0", graph_edges)
    #print(graph_dic)

    #internal_test_graph()

    #internal_get_spt_from_stat_name('CSE1', 'DOR72')

    pass

def get_ignore_stations():
    stats = {'S47A', 'GPO', 'G005', 'HW4', 'CS31A', 'RE22', 'RE27', 'BMU45',
            'CR100', 'CS46', 'CS55', 'CS57', 'CS58', 'CS59', 'CS60', 'CS62',
            'CS68', 'CS69', 'CS73', 'FLR3', 'GO21', 'GPO', 'J204', 'S47', 'CS40',
            'CS42','CS45','CS47','CS48','CS49','CS50','CS51','CS53','CS54',
            'CS61','CS72','DOR62','DOR63'}
    return stats

def preprocess():
    # Get road network
    graph_dic = gutil.get_graph(files.roads_pads_network_utm_geojson,
            files.roads_correction_utm_csv)
    #print(graph_dic)

    # Get station info
    stat_id_dic = gutil.create_station_status_dic(files.station_status_utm_geojson,
            files.closest_to_road_geojson_utm)
    remove_invalid_stations(stat_id_dic)
    #print('stations count', len(station_dic))
    #print(stat_id_dic)

    gutil.handle_road_not_found(stat_id_dic, graph_dic)
    #gutil.check_vertex_connected(graph_dic)

    # Add mapping to station info dictionary
    road_not_map_stat = add_station_to_road_mapping(stat_id_dic, graph_dic)
    print(len(road_not_map_stat), "stations can't find road mapping")

    # Get station name to id mapping
    #stat_name_dic = create_stat_name_id_mapping(stat_id_dic)

    # [Debug] Find the closest road of station that fail mapping
    #closest_road_list = gutil.find_closest_road(road_not_found_stat,
    #        station_dic, graph_dic)

    #print(stat_id_dic)
    sp_dic = get_spt_for_all_stations(stat_id_dic, graph_dic)
    gutil.write_dic_to_json(sp_dic, files.spt_json)

    return graph_dic, stat_id_dic

def remove_invalid_stations(stat_id_dic):
    ignore_stat_set = get_ignore_stations()
    for stat in list(stat_id_dic):
        if stat_id_dic[stat]['name'] in ignore_stat_set:
            del stat_id_dic[stat]

def get_all_stations_spt_dic_from_file():
    if not os.path.exists(files.spt_json):
        print("Havn't generate stations shortest path file!")
        return None
    with open(files.spt_json) as file:
        dic = json.load(file)
    #print(dic)
    return dic

def get_spt_for_all_stations(stat_id_dic, graph_dic):
    limit = '10'
    sp_dic = {}
    for id1 in stat_id_dic.keys():
        #print('id1', id1)
        #if id1 == limit:
        #    break
        for id2 in stat_id_dic.keys():
            #print('id2', id2)
            if id1 == id2:
                continue
            print('finding shortest path of', id1, '->', id2)
            path, dist = get_shortest_path_from_stat_id(id1, id2, stat_id_dic,
                    graph_dic)
            key = id1 + '#' + id2
            sp_dic[key] = {}
            sp_dic[key]['distance'] = dist
            sp_dic[key]['path'] = path
    return sp_dic
'''
def is_ready(stat_id, stat_id_dic):
    stat = stat_id_dic[stat_id]['name']
    road = stat_id_dic[stat_id]['road_id']
    not_ready_set = get_not_ready_station()
    if stat in not_ready_set or road == -1:
        print(stat_id, 'not ready')
        return False
    return True
'''
'''
def get_shortest_path_dist_from_stat(stat1, stat2, sp_dic):
    key = stat1 + '#' + stat2
    if key not in sp_dic:
        print('Stations cannot be found')
        return -1

    return sp_dic[key]['distance'], sp_dic['path']
'''
def internal_test_graph():
    test_graph_adj_dic = get_test_graph_dic()
    test_graph_edge_dic = get_test_graph_edge_dic()
    #print(test_graph_adj_dic)
    #print(test_graph_edge_dic)

    #print(test_graph_adj_dic['0']['adj'])

    internal_dijkstra('0', test_graph_adj_dic, test_graph_edge_dic)
    #print(test_graph_adj_dic)

    get_shortest_path('0', '4', test_graph_adj_dic)

def internal_dijkstra(src, graph_dic, dist_dic):
    if src not in graph_dic:
        print("src " + str(src) + " not in roads network")
        return
    vertices = set(graph_dic.keys())
    for vertex_id in graph_dic:
        #print(vertex_id)
        graph_dic[vertex_id]['dist'] = numpy.Inf
        graph_dic.get(vertex_id)['prev'] = -1
    graph_dic.get(src)['dist'] = 0

    #print(graph_dic)
    while vertices:
        min_dist_vertex, min_dist = get_min_dist(graph_dic, vertices)
        print('*** ', min_dist_vertex,':',  min_dist, '***')
        vertices.remove(min_dist_vertex)

        for neighbor in graph_dic.get(min_dist_vertex)['adj']:
            if neighbor in vertices:
                old_dist = graph_dic.get(neighbor)['dist']
                new_dist = (graph_dic.get(min_dist_vertex)['dist'] +
                    dist_dic[min_dist_vertex + '#' + neighbor])
                #print('old_dist', old_dist, 'new dist',new_dist)
                if new_dist < old_dist:
                    #print('update', neighbor)
                    graph_dic.get(neighbor)['dist'] = new_dist
                    graph_dic.get(neighbor)['prev'] = min_dist_vertex

def internal_get_spt_from_stat_name(station1, station2):
    #station1 = 'CSE1'
    #station2 = 'DOR72'
    not_ready_stat_set = get_not_ready_station()
    if station1 in not_ready_stat_set or station2 in not_ready_stat_set:
        print('stations closest road not ready yet')
        return

    graph_dic = gutil.get_graph(files.roads_pads_network_utm_geojson,
            files.roads_correction_utm_csv)
    #print(graph_dic)

    stat_id_dic = gutil.create_station_status_dic(files.station_status_utm_geojson,
            files.closest_to_road_geojson_utm )
    road_not_found_stat = add_station_to_road_mapping(stat_id_dic, graph_dic)
    stat_name_dic = create_stat_name_id_mapping(stat_id_dic)

    #internal_get_straight_dist_from_stats(station1, station2, stat_name_dic, stat_id_dic)

    id1 = stat_name_dic[station1]
    id2 = stat_name_dic[station2]
    path, dist = get_shortest_path_from_stat_id(id1, id2, stat_id_dic, graph_dic)
    print('Shortest path distance (m):', dist)
    print(path)

    return path, dist

def internal_get_straight_dist_from_stats(stat1, stat2, stat_name_dic, stat_id_dic):
    id1 = stat_name_dic[stat1]
    id2 = stat_name_dic[stat2]
    coord1 = stat_id_dic[id1]['coordinates']
    coord2 = stat_id_dic[id2]['coordinates']
    dist = gutil.calculate_dst_from_coordinates(coord1, coord2)
    print(stat1, stat2, dist)

def create_stat_name_id_mapping(station_dic):
    stat_name_dic = {}
    for stat_id in station_dic:
        stat_name = station_dic[stat_id]['name']
        stat_name_dic[stat_name] = stat_id
    return stat_name_dic

def get_shortest_path_from_stat_id(src_id, dst_id, station_dic, graph_dic):
    if src_id not in station_dic or dst_id not in station_dic:
        print('Invalid station id')
        return -100, -100
    road1_id = station_dic[src_id]['road_id']
    road2_id = station_dic[dst_id]['road_id']
    if road1_id == -1 or road2_id == -1:
        print(src_id, 'or', dst_id, 'do not have closest road')
        return -100, -100
    return get_shortest_path(road1_id, road2_id, graph_dic)

def add_station_to_road_mapping(station_dic, road_dic):
    stat_road_not_map_stat = []
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
            #print(station_dic[stat]['name'], 'closest road not map')
            stat_road_not_map_stat.append(stat)
    return stat_road_not_map_stat

def get_shortest_path(src, dst, graph_dic):
    dijkstra(src, graph_dic)
    path = get_dijkstra_path(src, dst, graph_dic)
    dist = graph_dic[dst]['dist']
    #print(path, dist)
    return path, dist
'''
def get_dist_from_path(path, graph_dic):
    total = 0
    for vertex in path:
        if vertex not in graph_dic:
            print('path vertex not in graph_dic')
            return -1
        else:
            total += graph_dic.get(vertex)['dist']
    return total
'''
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

def get_test_graph_dic():
    with open(files.test_graph_adj_csv) as csv_file:
        reader = csv.reader(csv_file)
        mydict = dict(reader)
        #print(mydict)
    for vertex in mydict:
        obj = eval(mydict[vertex])
        mydict[vertex] = obj
    return mydict

def get_test_graph_edge_dic():
    test_graph_edge_dic = {}
    with open(files.test_graph_edge_csv) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            #print(row)
            key1 = row['vertex1'] + '#' + row['vertex2']
            key2 = row['vertex2'] + '#' + row['vertex1']
            test_graph_edge_dic[key1] = int(row['edge'])
            test_graph_edge_dic[key2] = int(row['edge'])
    #print(test_graph_edge_dic)
    return test_graph_edge_dic

if __name__ == '__main__':
    main()
