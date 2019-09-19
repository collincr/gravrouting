import generate_road_adj_matrix as gram
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
        vertex_dic[vertex_id]['lon'] = key.split("#")[0]
        vertex_dic[vertex_id]['lat'] = key.split("#")[1]
    #print(vertex_dic)
    #write_dic_to_csv(vertex_dic)
    return vertex_dic

def dfs_recursive(vertex_id, vertex_dic):
    vertex_dic[vertex_id]['visited'] = True
    for adj_id in vertex_dic[vertex_id]['adj']:
        if not vertex_dic[adj_id]['visited']:
            dfs_recursive(adj_id, vertex_dic)

def dfs_iterative(vertex_id, vertex_dic):
    stack = [vertex_id]
    while stack:
        vertex = stack.pop()
        visited = vertex_dic[vertex]['visited']
        if not visited:
            vertex_dic[vertex]['visited'] = True
            for neighbor in vertex_dic[vertex]['adj']:
                stack.append(neighbor)

def check_vertex_connected(vertex_dic):
    count = 0
    for key in vertex_dic.keys():
        value = vertex_dic[key]
        if not value['visited']:
            count = count+1
            dfs_iterative(key, vertex_dic)
            #print(key, ": (", value['lon'],",", value['lat'],") not visited")
    return count

def write_dic_to_csv(dic):
     w = csv.writer(open("output.csv", "w"))
     for key, val in dic.items():
             w.writerow([key, val])

def write_dic_to_json(dic):
    json = json.dumps(dict)
    f = open("output.json","w")
    f.write(json)
    f.close()

#visited_vertex_dic = create_visited_vertex_dic(data_jasper_tmp_geojson)
visited_vertex_dic = create_visited_vertex_dic(roads_pads_network_geojson)
#dfs_recursive(4, visited_vertex_dic)
#dfs_iterative(4, visited_vertex_dic)
component_count = check_vertex_connected(visited_vertex_dic)
print(component_count)
#print(visited_vertex_dic)
write_dic_to_csv(visited_vertex_dic)
