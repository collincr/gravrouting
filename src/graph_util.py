import math
import csv
import json
import geopandas as gpd
import data_readin_conversion as drc

roads_pads_network_geojson = '../data/roads_pads_network_w_stations.geojson'
data_jasper_tmp_geojson = '../data/jasper_tmp.geojson'
roads_pads_network_UTM_geojson = '../data/roads_pads_network_w_stations_UTM.geojson'
roads_correction_csv = '../data/roads_correction.csv'
roads_correction_tmp_csv = '../data/roads_correction_tmp.csv'
roads_correction_UTM_csv = '../data/roads_correction_UTM.csv'

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
                        tmp_dic[key]['id'] = len(tmp_dic)-1 # start from 0
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
        vertex_adj_dic[vertex_id]['easting'] = int(key.split("#")[0])
        vertex_adj_dic[vertex_id]['northing'] = int(key.split("#")[1])
    return vertex_adj_dic, tmp_dic

def create_vertex_visit_dic(vertex_adj_dic):
    for key in vertex_adj_dic:
        vertex_adj_dic.get(key)['visited'] = False
    #print(vertex_adj_dic)
    return vertex_adj_dic
"""
def dfs_recursive(vertex_id, vertex_dic):
    vertex_dic[vertex_id]['visited'] = True
    for adj_id in vertex_dic[vertex_id]['adj']:
        if not vertex_dic[adj_id]['visited']:
            dfs_recursive(adj_id, vertex_dic)
"""
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

def check_vertex_connected(vertex_visit_dic):
    components = []
    for key in vertex_visit_dic.keys():
        value = vertex_visit_dic[key]
        if not value['visited']:
            path = []
            dfs_iterative(key, vertex_visit_dic, path)
            components.append(path)
            #print(key, ": (", value['easting'],",", value['northing'],") not visited")
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

def get_coord_from_vertex_id(vertex_id, vertex_visit_dic):
    if vertex_id in vertex_visit_dic:
        return vertex_visit_dic[vertex_id]['easting'], vertex_visit_dic[vertex_id]['northing']
    else:
        print("vertex:", vertex_id, "not exists")
        return 0,0

def calculate_dst(easting1, northing1, easting2, northing2):
    return math.sqrt(pow((easting1 - easting2), 2) + pow((northing1 - northing2), 2))

def get_dst_from_vertex_id(vertex_1, vertex_2, vertex_visit_dic):
    e1, n1 = get_coord_from_vertex_id(vertex_1, vertex_visit_dic)
    e2, n2 = get_coord_from_vertex_id(vertex_2, vertex_visit_dic)
    #print(vertex_1,"(", e1, n1, ")",)
    #print(vertex_2,"(", e2, n2, ")",)
    return calculate_dst(e1, n1, e2, n2)

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

def get_graph(roads_network_geoson, roads_correction_csv):
    vertex_adj_dic, tmp_dic = create_vertex_adj_dic(roads_network_geoson)
    add_correction_to_dic(roads_correction_csv, vertex_adj_dic, tmp_dic)
    vertex_visit_dic = create_vertex_visit_dic(vertex_adj_dic)

    # Remove invalid components
    components = check_vertex_connected(vertex_visit_dic)
    remove_component_from_dic(components[0], vertex_visit_dic)
    remove_component_from_dic(components[1], vertex_visit_dic)
    #print("Components count after removal:",len(components))

    # Check connectivity again
    vertex_visit_dic = create_vertex_visit_dic(vertex_visit_dic)
    components = check_vertex_connected(vertex_visit_dic)
    print("Components count after removal:",len(components))

    remove_item_from_dic('visited', vertex_visit_dic)
    return vertex_visit_dic


vertex_adj_dic = get_graph(roads_pads_network_UTM_geojson, roads_correction_UTM_csv)
#print(get_graph(data_jasper_tmp_geojson, roads_correction_tmp_csv))

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
