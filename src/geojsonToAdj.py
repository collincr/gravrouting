import geopandas as gpd
import json
import numpy as np

data_roads_pads_network = '../data/roads_pads_network.geojson'
data_jasper_tmp = '../data/jasper_tmp.geojson'

def pointToKey(p):
    key = str(int(p[0])) + "#" + str(int(p[1]))
    #print(key)
    return key

vertex_dic = {}
with open(data_roads_pads_network) as f:
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

#print(vertex_dic)
#print(len(vertex_dic))

n = len(vertex_dic)
adjMatrix = [[0 for x in range(n)] for y in range(n)]

vertex_infos = vertex_dic.values()
for vertex_info in vertex_infos:
    #print(vertex_info)
    vertex_id = vertex_info['id']
    for j in range(n):
        if j in vertex_info['adj']:
            adjMatrix[vertex_id][j] = 1

#print(adjMatrix)
#print(np.matrix(adjMatrix))

mat = np.matrix(adjMatrix)
with open('output_adjMtx.txt','wb') as f:
    for line in mat:
        np.savetxt(f, line, '%i')
