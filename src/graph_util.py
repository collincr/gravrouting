import math
import csv
import json
import geopandas as gpd
import data_readin_conversion as drc
import files
import numpy

def main():

    #vertex_adj_dic = get_graph(roads_pads_network_UTM_geojson, roads_correction_UTM_csv)
    #print(get_graph(data_jasper_tmp_geojson, roads_correction_tmp_csv))

    # convert geojson to utm form
    #gdf_utm = drc.convert_to_UTM_with_geojson(files.closest_to_road_goejson)
    #drc.geojson_saver(gdf_utm, files.closest_to_road_geojson_utm)

    #internal_get_perpendicular_distance()
    #internal_get_closest_point_to_line()
    pass

def create_vertex_adj_dic(geojson_file):
    tmp_dic = {}
    with open(geojson_file) as f:
    #with open(data_jasper_tmp) as f:
        data = json.load(f)
    for feature in data['features']:
        #print("+++ FEATURE +++")
        if (feature['geometry'] is not None and
            feature['geometry']['coordinates'] is not None):
            for line in feature['geometry']['coordinates']:
                #print("*** LINE ***")
                #print(line)
                for i in range(len(line)):
                    point = line[i]
                    key = pointToKey(point)
                    point_info = tmp_dic.get(key)
                    if point_info is None:
                        tmp_dic[key] = {}
                        tmp_dic[key]['id'] = str(len(tmp_dic)-1) # start from 0
                        tmp_dic[key]['adj'] = set()
                        point_info = tmp_dic[key]

                    if i > 0:
                        left_key = pointToKey(line[i-1])
                        left_point_info = tmp_dic.get(left_key)
                        if left_point_info is not None:
                            point_info['adj'].add(left_point_info['id'])
                            left_point_info['adj'].add(tmp_dic[key]['id'])
                        else:
                            print("Left point is None!")
    vertex_adj_dic = {}
    for key in tmp_dic.keys():
        #print(value['id'])
        #print(key.split("#")[0])
        value = tmp_dic[key]
        vertex_id = value['id']
        vertex_adj_dic[vertex_id] = {}
        vertex_adj_dic[vertex_id]['adj'] = value['adj']
        vertex_adj_dic[vertex_id]['coordinates'] = [int(key.split("#")[0]),
                int(key.split("#")[1])]
    return vertex_adj_dic, tmp_dic

def reset_vertex_visit_dic(vertex_adj_dic):
    for key in vertex_adj_dic:
        vertex_adj_dic.get(key)['visited'] = False
    #print(vertex_adj_dic)
    return vertex_adj_dic
'''
def dfs_recursive(vertex_id, vertex_dic):
    vertex_dic[vertex_id]['visited'] = True
    for adj_id in vertex_dic[vertex_id]['adj']:
        if not vertex_dic[adj_id]['visited']:
            dfs_recursive(adj_id, vertex_dic)
'''
def dfs_iterative(vertex_id, vertex_visit_dic, path):
    stack = [vertex_id]
    while stack:
        vertex = stack.pop()
        visited = vertex_visit_dic[vertex]['visited']
        if not visited:
            path.append(vertex)
            vertex_visit_dic[vertex]['visited'] = True
            for neighbor in vertex_visit_dic[vertex]['adj']:
                stack.append(neighbor)

def bfs_iterative(coordinate, src, vertex_visit_dic):
    queue = [src]
    min_dist = numpy.Inf
    edge = []
    closest_coord = [-1, -1]
    while queue:
        vertex = queue.pop(0)
        if not vertex_visit_dic[vertex]['visited']:
            vertex_visit_dic[vertex]['visited'] = True
            for adj in vertex_visit_dic[vertex]['adj']:
                dist = get_perpendicular_distance(coordinate, [vertex, adj],
                        vertex_visit_dic)
                coord = get_closest_point_on_line(coordinate, [vertex, adj],
                        vertex_visit_dic)
                if dist < min_dist:
                    min_dist = dist
                    edge = [vertex, adj]
                    closest_coord = coord
                queue.append(adj)
    return closest_coord, edge

def check_vertex_connected(vertex_adj_dic):
    components = []
    reset_vertex_visit_dic(vertex_adj_dic)
    for key in vertex_adj_dic.keys():
        value = vertex_adj_dic[key]
        if not value['visited']:
            path = []
            dfs_iterative(key, vertex_adj_dic, path)
            components.append(path)
            #print(key, ": (", value['easting'],",", value['northing'],") not visited")
    remove_item_from_dic('visited', vertex_adj_dic)
    return components

def write_dic_to_csv(dic):
     w = csv.writer(open("output.csv", "w"))
     for key, val in dic.items():
             w.writerow([key, val])

def write_dic_to_json(dic):
    output = json.dumps(dict)
    f = open("output.json","w")
    f.write(output)
    f.close()

def get_coord_from_vertex_id(vertex_id, vertex_visit_dic):
    if vertex_id in vertex_visit_dic:
        coordinates = vertex_visit_dic[vertex_id]['coordinates']
        return coordinates[0], coordinates[1]
    else:
        print("vertex:", vertex_id, "not exists")
        return 0,0

def calculate_dst(easting1, northing1, easting2, northing2):
    return math.sqrt(pow((easting1 - easting2), 2) + pow((northing1 - northing2), 2))

def calculate_dst_from_coordinates(coordinates1, coordinates2):
    return math.sqrt(pow((coordinates1[0] - coordinates2[0]), 2)
            + pow((coordinates1[1] - coordinates2[1]), 2))

def get_dst_from_vertex_id(vertex_1, vertex_2, vertex_visit_dic):
    e1, n1 = get_coord_from_vertex_id(vertex_1, vertex_visit_dic)
    e2, n2 = get_coord_from_vertex_id(vertex_2, vertex_visit_dic)
    dist = calculate_dst(e1, n1, e2, n2)
    #print(vertex_1,"(", e1, n1, ")", vertex_2,"(", e2, n2, ")", dist)
    return dist
    #return calculate_dst(e1, n1, e2, n2)

def print_kth_componenet(k, components, with_coord, vertex_visit_dic):
    print("component " + str(k))
    if k >= len(components):
        print("k is out of bound")
        return
    if with_coord:
        for vertex in components[k]:
            print(vertex, get_coord_from_vertex_id(vertex, vertex_visit_dic))
    else:
        print(components[k])

def check_same_vertex(distance, components, vertex_visit_dic):
    for cur_comp in range(len(components)):
        for other_comp in range(cur_comp + 1, len(components)):
            for cur_vertex in components[cur_comp]:
                for other_vertex in components[other_comp]:
                    dis = get_dst_from_vertex_id(cur_vertex, other_vertex, vertex_visit_dic)
                    if dis < distance:
                        #print(cur_vertex, other_vertex, " are close")
                        print(cur_vertex,
                            get_coord_from_vertex_id(cur_vertex, vertex_visit_dic),
                            " in comp-" + str(cur_comp),",", other_vertex,
                            get_coord_from_vertex_id(other_vertex, vertex_visit_dic),
                            " in comp-" + str(other_comp) + " are close")

def find_closest_road(stat_list, stat_dic, road_dic):
    closest_road_list = []
    for stat in stat_list:
        stat_coordinate = stat_dic[stat]['coordinates']
        min_dist = numpy.Inf
        road_id = -1
        for road in road_dic:
            road_coordinate = road_dic[road]['coordinates']
            dist = calculate_dst_from_coordinates(stat_coordinate, road_coordinate)
            if dist < min_dist:
                min_dist = dist
                road_id = road
        #print(min_dist)
        closest_road_list.append(road_id)
    return closest_road_list

def get_component_from_coord(easting, northing, components, vertex_visit_dic):
    for i in range(len(components)):
        for vertex in components[i]:
            e, n = get_coord_from_vertex_id(vertex, vertex_visit_dic)
            if easting == e and northing == n:
                return i
    return -1


def pointToKey(p):
    key = str(int(p[0])) + "#" + str(int(p[1]))
    #print(key)
    return key

def create_adj_matrix(vertex_adj_dictionary):
    n = len(vertex_adj_dictionary)
    adj_matrix = [[0 for x in range(n)] for y in range(n)]
    vertex_infos = vertex_adj_dictionary.values()
    for vertex_info in vertex_infos:
        #print(vertex_info)
        vertex_id = vertex_info['id']
        for j in range(n):
            if j in vertex_info['adj']:
                adj_matrix[vertex_id][j] = 1
    return adj_matrix

def write_matrix_to_file(matrix):
    mat = np.matrix(matrix)
    with open('../resources/file/output_adj_mtx.txt','wb') as f:
        for line in mat:
            np.savetxt(f, line, '%i')

def add_adj_vertex(vertex1, vertex2, vertex_adj_dic, coord_to_id_dic):

    key1 = pointToKey(vertex1)
    key2 = pointToKey(vertex2)
    if key1 not in coord_to_id_dic or key2 not in coord_to_id_dic:
        print(key1 + " or " + key2 + " not in coord_to_id_dic")
    else:
        #print(vertex_dic[key1])
        #coord_to_id_dic[key1]['adj'].add(coord_to_id_dic.get(key2)['id'])
        #coord_to_id_dic[key2]['adj'].add(coord_to_id_dic.get(key1)['id'])
        id1 = coord_to_id_dic.get(key1)['id']
        id2 = coord_to_id_dic.get(key2)['id']
        vertex_adj_dic.get(id1)['adj'].add(id2)
        vertex_adj_dic.get(id2)['adj'].add(id1)

def add_correction_to_dic(file_name, vertex_adj_dic, coord_to_id_dic):
    with open(file_name, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=',')
        for row in csv_reader:
            v1 = [row['Easting1'], row['Northing1']]
            v2 = [row['Easting2'], row['Northing2']]
            add_adj_vertex(v1, v2, vertex_adj_dic, coord_to_id_dic)
            
def remove_component_from_dic(comp, vertex_visit_dic):
    for vertex_id in comp:
        if vertex_id in vertex_visit_dic:
            #print("delete " + str(vertex_id) + " from vertex_visit_dic")
            del vertex_visit_dic[vertex_id]
        else:
            print("vertex " + str(vertex_id) + " not in vertex_visit_dic")

def remove_item_from_dic(item_name, vertex_dic):
    for key in vertex_dic:
        value = vertex_dic.get(key)
        if item_name in value:
            del value[item_name]
'''
Create road network dictionary contains entries as below
id:
{
    adj: {adjacent vertices id},
    coordinates: [easting, northing]
}
'''
def get_graph(roads_network_geoson, roads_correction_csv):
    vertex_adj_dic, tmp_dic = create_vertex_adj_dic(roads_network_geoson)
    add_correction_to_dic(roads_correction_csv, vertex_adj_dic, tmp_dic)

    # Remove invalid components
    components = check_vertex_connected(vertex_adj_dic)
    remove_component_from_dic(components[0], vertex_adj_dic)
    remove_component_from_dic(components[1], vertex_adj_dic)
    #print("Components count after removal:",len(components))

    # Check connectivity again
    components = check_vertex_connected(vertex_adj_dic)
    print("Components count after removal:",len(components))
    #print(vertex_adj_dic)

    return vertex_adj_dic

'''
Create station info dictionary contains entries as below
id:
{
    'name': 'RE37',
    'type': 0,
    'status': 'Found',
    'coordinates': [easting, northing],
    'road_coordinates': [easting, northing, elevation]
}
'''
def create_station_status_dic(stat_id_geojson, stat_road_geojson):
    # Get closest road coordinates
    station_road_dic = {}
    with open(stat_road_geojson) as f:
        station_road_info = json.load(f)
    for feature in station_road_info['features']:
        station_name = feature['properties']['NAME']
        station_road_coord = feature['geometry']['coordinates']
        station_road_dic[station_name] = station_road_coord

    # Get station id, status, utm coordinate
    station_id_dic = {}
    with open(stat_id_geojson) as f:
        station_id_info = json.load(f)
    for feature in station_id_info['features']:
        station_id = str(feature['properties']['StationNumber'])
        station_name = feature['properties']['StationName']
        station_type = feature['properties']['StationType']
        station_status = feature['properties']['Status']
        station_coord = feature['geometry']['coordinates']

        station_id_dic[station_id] = {}
        station_id_dic[station_id]['name'] = station_name
        station_id_dic[station_id]['type'] = station_type
        station_id_dic[station_id]['status'] = station_status
        station_id_dic[station_id]['coordinates'] = station_coord
        if station_name in station_road_dic:
            station_id_dic[station_id]['road_coordinates'] = station_road_dic[station_name]
        else:
            #print(station_name, "closest road not found")
            station_id_dic[station_id]['road_coordinates'] = [-1, -1]

    return station_id_dic

def handle_road_not_found(station_id_dic, vertex_adj_dic):
    for stat in station_id_dic:
        road_coord = station_id_dic[stat]['road_coordinates']
        if road_coord[0] == -1 and road_coord[1] == -1:
            reset_vertex_visit_dic(vertex_adj_dic)
            src = next(iter(vertex_adj_dic)) # first vertex
            closest_coordinate, edge = bfs_iterative(station_id_dic[stat]['coordinates'],
                    src, vertex_adj_dic)
            station_id_dic[stat]['road_coordinates'] = closest_coordinate
            add_vertex_to_road_network(edge, closest_coordinate, vertex_adj_dic)
    remove_item_from_dic('visited', vertex_adj_dic)

def get_perpendicular_distance(point, edge, vertex_adj_dic):
   coord1 = vertex_adj_dic[edge[0]]['coordinates']
   coord2 = vertex_adj_dic[edge[1]]['coordinates']
   denominator = calculate_dst_from_coordinates(coord1, coord2)
   numerator = abs((coord2[1] - coord1[1]) * point[0] - (coord2[0] - coord1[0]) * point[1] + coord2[0] * coord1[1] - coord2[1] * coord1[0])

   return (numerator / denominator)

def get_closest_point_on_line(point, edge, vertex_adj_dic):
    coord1 = vertex_adj_dic[edge[0]]['coordinates']
    coord2 = vertex_adj_dic[edge[1]]['coordinates']
    coord1_to_point = [point[0] - coord1[0], point[1] - coord1[1]]
    coord1_to_coord2 = [coord2[0] - coord1[0], coord2[1] - coord1[1]]
    dist_square = pow(coord1_to_coord2[0], 2) + pow(coord1_to_coord2[1], 2)
    dot_product = (coord1_to_point[0]*coord1_to_coord2[0]
            + coord1_to_point[1]*coord1_to_coord2[1])
    normalized_dist = dot_product / dist_square
    closest_point = [coord1[0] + coord1_to_coord2[0] * normalized_dist,
            coord1[1] + coord1_to_coord2[1] * normalized_dist]
    print('closest point:', closest_point[0], closest_point[1])
    return closest_point

def internal_get_perpendicular_distance(coord1, coord2, point):
    coord1 = [5, 8]
    coord2 = [10, 14]
    point = [-3, 7]
    denominator = calculate_dst_from_coordinates(coord1, coord2)
    numerator = abs((coord2[1] - coord1[1]) * point[0] - (coord2[0] - coord1[0]) * point[1] + coord2[0] * coord1[1] - coord2[1] * coord1[0])
    #print(numerator / denominator)
    return numerator / denominator

def internal_get_closest_point_on_line(coord1, coord2, point):
    coord1 = [5, -21]
    coord2 = [10, -51]
    point = [3, 8]
    coord1_to_point = [point[0] - coord1[0], point[1] - coord1[1]]
    coord1_to_coord2 = [coord2[0] - coord1[0], coord2[1] - coord1[1]]
    dist_square = pow(coord1_to_coord2[0], 2) + pow(coord1_to_coord2[1], 2)
    dot_product = (coord1_to_point[0]*coord1_to_coord2[0]
            + coord1_to_point[1]*coord1_to_coord2[1])
    normalized_dist = dot_product / dist_square
    closest_point = [coord1[0] + coord1_to_coord2[0] * normalized_dist,
            coord1[1] + coord1_to_coord2[1] * normalized_dist]
    #print('closest point:', closest_point[0], closest_point[1])
    return closest_point

def add_vertex_to_road_network(edge, vertex_coord, vertex_adj_dic):
    id = get_max_id(vertex_adj_dic) + 1
    remove_adj(edge[0], edge[1], vertex_adj_dic)
    remove_adj(edge[1], edge[0], vertex_adj_dic)
    vertex_adj_dic[id] = {}
    vertex_adj_dic[id]['coordinates'] = vertex_coord
    vertex_adj_dic[id]['adj'] = {edge[0], edge[1]}

def get_max_id(vertex_adj_dic):
    max_id = -1
    for vertex_id in vertex_adj_dic:
        max_id = max(max_id, vertex_id)
    return max_id

def remove_adj(vertex, adj, vertex_adj_dic):
    if vertex not in vertex_adj_dic:
        print('vertex', vertex, 'not in vertex_adj_dic')
        return
    if adj in vertex_adj_dic[vertex]['adj']:
        vertex_adj_dic[vertex]['adj'].remove(adj)
    else:
        print('adj not found')

if __name__ == '__main__':
    main()

"""
gdf_utm = drc.convert_to_UTM_with_geojson(roads_pads_network_geojson)
drc.geojson_saver(gdf_utm, roads_pads_network_UTM_geojson)
"""


"""
# Create (k, v) = (id, adj set) dictionary
vertex_adj_dic, tmp_dic = create_vertex_adj_dic(roads_pads_network_UTM_geojson)
#vertex_adj_dic, tmp_dic = create_vertex_adj_dic(data_jasper_tmp_geojson)
#print(vertex_adj_dic)

# Add vertices correction
add_correction_to_dic(roads_correction_UTM_csv, vertex_adj_dic, tmp_dic)
#add_correction_to_dic(roads_correction_tmp_csv, vertex_adj_dic, tmp_dic)
#print(vertex_adj_dic)
#matrix = create_adj_matrix(vertex_dictionary)

# Create (k, v) = (id, {adj set, visited}) dictionary
vertex_visit_dic = create_vertex_visit_dic(vertex_adj_dic)
components = check_vertex_connected(vertex_visit_dic)
print("Components count before removal:",len(components))

# Check if there is a vertex but has two different coordinates
#max_dst = 10
#check_same_vertex(max_dst, components, vertex_visit_dic)
#print_kth_componenet(3, components, True, vertex_visit_dic)

# get component number
#comp1 = get_component_from_coord(431670, 3976576, components, vertex_visit_dic)
#comp2 = get_component_from_coord(430486, 3976875, components, vertex_visit_dic)
#print("comp1", comp1, " comp2", comp2)

# Remove invalid vertices components
#print("dic count before:", len(vertex_visit_dic))
remove_component_from_dic(components[0], vertex_visit_dic)
remove_component_from_dic(components[1], vertex_visit_dic)
#print("dic count after:", len(vertex_visit_dic))

# Check connectivity again
vertex_visit_dic = create_vertex_visit_dic(vertex_visit_dic)
components = check_vertex_connected(vertex_visit_dic)
print("Components count after removal:",len(components))
#print(vertex_visit_dic)
"""
