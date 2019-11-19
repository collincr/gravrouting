import numpy as np
import itertools
import datetime as dt
from cluster_by_agglomerative import get_cluster_dic
from cluster_by_agglomerative import find_cluster_adj
from cluster_by_agglomerative import plot_clustering_from_dic
from cluster_routing import route_with_sequence

def main():

    # generate 19 different cluster
    cluster_stat_dic = get_cluster_dic()

    # aggregate small clusters 
    updated_cluster_dic = aggregate_cluster(cluster_stat_dic)

    print("Aggregated cluster is: ")
    print(updated_cluster_dic)

    updated_cluster_dic = find_cluster_adj(updated_cluster_dic)
    
    # file_path = '../resources/file/permutations.txt'
    # cluster_seqs = []
    # try:
    #     with open(file_path, 'r') as f:
    #         for line in f:
    #             # remove linebreak which is the last character of the string
    #             currentPermutation = line[:-1]
    #             # add item to the list
    #             cluster_seqs.append(currentPermutation)
    # except IOError:
    #     print("\nGenerating permuations...")
    #     cluster_seqs = permutations(len(updated_cluster_dic))
    #     print("Finished generation of permuations.")
    #     with open(file_path, 'w') as f:
    #         for listitem in cluster_seqs:
    #             f.write('%s\n' % str(listitem))

    #cluster_seq = ['0', '8', '5', '11', '6', '7', '10', '9', '1', '2', '3', '4']
    cluster_seq = ['10', '7', '9', '4', '0', '5', '1', '2', '3', '6', '8', '11']
    total_times = route_with_sequence(cluster_seq, updated_cluster_dic)
    res = {}
    day = 1
    begin_stat_idx_of_the_day = 0
    time_of_days_before = 0
    for i in range(len(total_times)):
        time = total_times[i]
        if dt.timedelta(seconds=time) > dt.timedelta(hours=8):
            one_day = {}
            clusters_for_each_day = cluster_seq[begin_stat_idx_of_the_day, i]
            one_day['clusters'] = clusters_for_each_day
            seconds = time - time_of_days_before
            one_day['time'] = dt.timedelta(seconds=seconds)
            time_of_days_before += time
            begin_stat_idx_of_the_day = i
            day += 1
    print(res)

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


def permutations(len):
    cluster_ids = [str(x) for x in range(0, len)]
    print(cluster_ids)
    perm = list(itertools.permutations(cluster_ids))
    return perm


if __name__ == '__main__':
    main()
