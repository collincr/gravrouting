import geopandas as gpd
import json
import numpy as np

data_roads_pads_network = '../data/roads_pads_network_w_stations.geojson'
data_jasper_tmp = '../data/jasper_tmp.geojson'

def pointToKey(p):
    key = str(int(p[0])) + "#" + str(int(p[1]))
    #print(key)
    return key

def create_adj_vertex_dic(geojson_file):
    vertex_dic = {}
    with open(geojson_file) as f:
    #with open(data_jasper_tmp) as f:
        data = json.load(f)
    for feature in data['features']:
        #print("+++ FEATURE +++")
        for line in feature['geometry']['coordinates']:
            #print("*** LINE ***")
            #print(line)
            for i in range(len(line)):
                point = line[i]
                key = pointToKey(point)
                point_info = vertex_dic.get(key)
                if point_info is None:
                    vertex_dic[key] = {}
                    vertex_dic[key]['id'] = len(vertex_dic)-1 # start from 0
                    vertex_dic[key]['adj'] = set()
                    point_info = vertex_dic[key]

                if i > 0:
                    left_key = pointToKey(line[i-1])
                    left_point_info = vertex_dic.get(left_key)
                    if left_point_info is not None:
                        point_info['adj'].add(left_point_info['id'])
                        left_point_info['adj'].add(vertex_dic[key]['id'])
                    else:
                        print("Left point is None!")
    return vertex_dic

def create_adj_matrix(vertex_adj_dictionary):
    n = len(vertex_adj_dictionary)
    adj_matrix = [[0 for x in range(n)] for y in range(n)]
    vertex_infos = vertex_dictionary.values()
    for vertex_info in vertex_infos:
        #print(vertex_info)
        vertex_id = vertex_info['id']
        for j in range(n):
            if j in vertex_info['adj']:
                adj_matrix[vertex_id][j] = 1
    return adj_matrix
"""
vertex_dictionary = create_adj_vertex_dic(data_roads_pads_network)
matrix = create_adj_matrix(vertex_dictionary)
mat = np.matrix(matrix)
with open('../resources/file/output_adj_mtx.txt','wb') as f:
    for line in mat:
        np.savetxt(f, line, '%i')

"""
