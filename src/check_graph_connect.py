import generate_road_adj_matrix as gram
import math
import csv

roads_pads_network_geojson = '../data/roads_pads_network_w_stations.geojson'
data_jasper_tmp_geojson = '../data/jasper_tmp.geojson'

def create_visited_vertex_dic(geojson_file):

    tmp_vertex_dic = gram.create_adj_vertex_dic(geojson_file)
    vertex_dic = {}
    #for value in tmp_vertex_dic.values():
    for key in tmp_vertex_dic.keys():
        #print(value['id'])
        #print(key.split("#")[0])
        value = tmp_vertex_dic[key]
        vertex_id = value['id']
        vertex_dic[vertex_id] = {}
        vertex_dic[vertex_id]['adj'] = value['adj']
        vertex_dic[vertex_id]['visited'] = False
        vertex_dic[vertex_id]['lon'] = int(key.split("#")[0])
        vertex_dic[vertex_id]['lat'] = int(key.split("#")[1])
    #print(vertex_dic)
    write_dic_to_csv(vertex_dic)
    return vertex_dic

def dfs_recursive(vertex_id, vertex_dic):
    vertex_dic[vertex_id]['visited'] = True
    for adj_id in vertex_dic[vertex_id]['adj']:
        if not vertex_dic[adj_id]['visited']:
            dfs_recursive(adj_id, vertex_dic)

def dfs_iterative(vertex_id, vertex_dic, path):
    stack = [vertex_id]
    while stack:
        vertex = stack.pop()
        visited = vertex_dic[vertex]['visited']
        if not visited:
            path.append(vertex)
            vertex_dic[vertex]['visited'] = True
            for neighbor in vertex_dic[vertex]['adj']:
                stack.append(neighbor)

def check_vertex_connected(vertex_dic):
    components = []
    for key in vertex_dic.keys():
        value = vertex_dic[key]
        if not value['visited']:
            path = []
            dfs_iterative(key, vertex_dic, path)
            components.append(path)
            #print(key, ": (", value['lon'],",", value['lat'],") not visited")
    return components

def write_dic_to_csv(dic):
     w = csv.writer(open("output.csv", "w"))
     for key, val in dic.items():
             w.writerow([key, val])

def write_dic_to_json(dic):
    json = json.dumps(dict)
    f = open("output.json","w")
    f.write(json)
    f.close()

def get_coord_from_vertex_id(vertex_id, vertex_dic):
    if vertex_id in vertex_dic:
        return vertex_dic[vertex_id]['lon'], vertex_dic[vertex_id]['lat']
    else:
        print("vertex:", vertex_id, "not exists")
        return 0,0

def calculate_dst(lon1, lat1, lon2, lat2):
    return math.sqrt(pow((lon1 - lon2), 2) + pow((lat1 - lat2), 2))

def get_dst_from_vertex_id(vertex_1, vertex_2, vertex_dic):
    lon1, lat1 = get_coord_from_vertex_id(vertex_1, vertex_dic)
    lon2, lat2 = get_coord_from_vertex_id(vertex_2, vertex_dic)
    #print(vertex_1,"(", lon1, lat1, ")",)
    #print(vertex_2,"(", lon2, lat2, ")",)
    return calculate_dst(lon1, lat1, lon2, lat2)

def print_kth_componenet(k, components, with_coord, vertex_dic):
    print("component " + str(k))
    if with_coord:
        for vertex in components[k]:
            print(get_coord_from_vertex_id(vertex, vertex_dic))
    else:
        print(components[k])

def check_same_vertex(distance, components):
    for cur_comp in range(len(components)):
        for other_comp in range(cur_comp + 1, len(components)):
            for cur_vertex in components[cur_comp]:
                for other_vertex in components[other_comp]:
                    dis = get_dst_from_vertex_id(cur_vertex, other_vertex,
                            visited_vertex_dic)
                    if dis < max_distance:
                        #print(cur_vertex, other_vertex, " are close")
                        print(cur_vertex,
                            get_coord_from_vertex_id(cur_vertex, visited_vertex_dic),
                            " in comp-" + str(cur_comp),",", other_vertex,
                            get_coord_from_vertex_id(other_vertex, visited_vertex_dic),
                            " in comp-" + str(other_comp) + " are close")


def get_component_from_coord(easting, northing, components, vertex_dic):
    for i in range(len(components)):
        for vertex in components[i]:
            e, n = get_coord_from_vertex_id(vertex, vertex_dic)
            if easting == e and northing == n:
                return i
    return -1

#visited_vertex_dic = create_visited_vertex_dic(data_jasper_tmp_geojson)
visited_vertex_dic = create_visited_vertex_dic(roads_pads_network_geojson)
#print(visited_vertex_dic)
#write_dic_to_csv(visited_vertex_dic)

#dfs_recursive(4, visited_vertex_dic)
#dfs_iterative(5, visited_vertex_dic, path)

#print(get_dst_from_vertex_id(0, 1, visited_vertex_dic))

components = check_vertex_connected(visited_vertex_dic)
max_distance = 33
#print_kth_componenet(1, components, True, visited_vertex_dic)
#print("Components count:",len(components))
check_same_vertex(max_distance, components)
#comp = get_component_from_coord(2354350, 258324, components, visited_vertex_dic)
#print(comp)
