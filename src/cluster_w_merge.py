import numpy as np
import time
from cluster_by_agglomerative import get_cluster_dic
from cluster_by_agglomerative import find_cluster_adj
from cluster_by_agglomerative import plot_clustering_from_dic

def main():

    # generate 19 different cluster
    cluster_stat_dic = get_cluster_dic()

    # aggregate small clusters 
    updated_cluster_dic = aggregate_cluster(cluster_stat_dic)

    plot_clustering_from_dic(updated_cluster_dic)


def aggregate_cluster(cluster_stat_dic):

    updated_cluster_dic = {}
    index = 0

    # directly add cl1, cl2, cl6, cl11, cl17
    indexList = [1, 2, 6, 11, 17]
    for formerIndex in indexList:
        updated_cluster_dic[str(index)] = cluster_stat_dic[str(formerIndex)]
        index += 1

    # merge clusters together
    id_list = [
        [3, 4, 18],     # cl18 + cl4 + cl3 -> new cl3 (size 9 stations)
        [5, 15],        # cl15 + cl5 -> new cl5 (size 10 stations)
        [7, 8],         # cl7 + cl8 -> new cl8 (size 11 stations)
        [12, 19]        # cl12 + cl19 -> new cl19 (size 9 stations)
    ]
    for ids in id_list:
        updated_cluster_dic[str(index)] = create_new_station_list(ids, cluster_stat_dic)
        index += 1

    # split cluster and add stations to clusters
    ids = [9, 10]       # cl9 + cl10 + 2 stations in cl13 -> new cl9 (size 10 stations)
    tmp_stations_1 = create_new_station_list(ids, cluster_stat_dic)
    stations_to_add = np.array(['115', '149'])
    tmp_stations_1['stations'] = np.append(tmp_stations_1['stations'], stations_to_add)
    updated_cluster_dic[str(index)] = tmp_stations_1
    index += 1

    # 7 stations in cl0 + cl16 -> new cl16 (size 10 stations)
    cluster_0 = cluster_stat_dic['0']['stations']
    part_of_cluster_0 = cluster_0[(cluster_0 != '11') & (cluster_0 != '72')]
    merged_2 = np.append(cluster_stat_dic['16']['stations'], part_of_cluster_0)
    tmp_stations_2 = {}
    tmp_stations_2['stations'] = merged_2
    updated_cluster_dic[str(index)] = tmp_stations_2
    index += 1

    # 2 stations in cl0 + cl14 + 5 stations in cl13  -> new cl14 (size 7 stations)
    cluster_13 = cluster_stat_dic['13']['stations']
    part_of_cluster_13 = cluster_13[(cluster_13 != '115') & (cluster_13 != '149')]
    merged_3 = np.append(cluster_stat_dic['14']['stations'], part_of_cluster_13)
    stations_to_add = np.array(['11', '72'])
    merged_3 = np.append(merged_3, stations_to_add)
    tmp_stations_3 = {}
    tmp_stations_3['stations'] = merged_3
    updated_cluster_dic[str(index)] = tmp_stations_3

    return updated_cluster_dic


def create_new_station_list(ids, cluster_stat_dic):
    merged = []
    for id in ids:
        tmp = cluster_stat_dic[str(id)]['stations']
        merged = np.append(merged, tmp)

    tmp_stations = {}
    tmp_stations['stations'] = merged
    return tmp_stations


if __name__ == '__main__':
    main()
