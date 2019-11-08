import numpy as np
import shortest_path as sp

from sklearn.cluster import AgglomerativeClustering

def main():
    get_cluster_dic()
    pass

def get_cluster_dic():
    station_dic = sp.get_station_dic()
    dist_matrix = compute_dis_matrix()

    cluster_number = 11
    cluster_labels = agglomerative_clustering(cluster_number, dist_matrix)
    print(cluster_labels)
    
    stat_list = np.array(list(station_dic.keys()))
    cluster_stat_dic = {}
    for i in range(0, cluster_number):
        cluster_stat_dic[str(i)] = stat_list[cluster_labels==i]

    print(cluster_stat_dic)
    #print(cluster_stat_dic['0'])
    return cluster_stat_dic

def agglomerative_clustering(cluster_num, dist_matrix):
    hc = AgglomerativeClustering(n_clusters=cluster_num, affinity = 'precomputed',
            linkage = 'average')
    y_hc = hc.fit_predict(dist_matrix)
    #print(len(dist_matrix))
    #print(len(y_hc))
    #print(y_hc)
    #print(y_hc[y_hc==1])
    return y_hc

def compute_dis_matrix():
    station_dic = sp.get_station_dic()
    dist_matrix = [([0] * len(station_dic)) for i in range(len(station_dic))]
    stations_shortest_path_dic = sp.get_all_stations_spt_dic_from_file()

    row = 0
    stat_id_to_index = {}
    for stat_id in station_dic:
        stat_id_to_index[stat_id] = row
        row += 1

    for stat_id1 in station_dic:
        for stat_id2 in station_dic:
            if stat_id1 is not stat_id2:
                distance = 0
                key = stat_id1 + "#" + stat_id2
                #print(key)
                distance, path = sp.get_shortest_path_from_stat_id(stat_id1, stat_id2,
                        station_dic, stations_shortest_path_dic)
                if distance == None:
                    print("Coundn't find distance in file, calculate again")
                    path, distance = internal_get_spt_from_stat_name(
                            station_dic[stat_id1]['name'], station_dic[stat_id2]['name'])
                
                idx1 = stat_id_to_index[stat_id1]
                idx2 = stat_id_to_index[stat_id2]
                dist_matrix[idx1][idx2] = distance
                dist_matrix[idx2][idx1] = distance
    #print(dist_matrix)
    return dist_matrix

if __name__ == '__main__':
    main()
