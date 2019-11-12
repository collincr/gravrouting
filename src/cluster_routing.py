import cluster_by_agglomerative as cba
import shortest_path as sp
import graph_util as gutil
import station_routing as sr
import datetime
import datetime as dt
import time
import itertools


def main():
    print(str(dt.timedelta(seconds = time.time())))
    cluster_adj_dic = cba.get_cluster_adj_dic()
    # print(cluster_adj_dic)
    #get_cluster_permutation(cluster_adj_dic, True)
    cluster_seq = ['0', '8', '14', '13', '12', '5', '15', '11', '6', '7', '10',
            '9', '17', '1', '2', '3', '4', '18', '19', '16']
    # route_with_sequence(cluster_seq)
    get_cluster_permutations(cluster_adj_dic)
    print(str(dt.timedelta(seconds = time.time())))
    '''
    perms = []
    dic = {}
    for i in range(0, 20):
        dic[i] = i
    helper([], perms, dic)
    '''
    pass

def get_cluster_permutations(cluster_adj_dic):
    cluster_ids = ['0','1','2','3','4','5','6','7','8','9','10','11']
    l = list(itertools.permutations(cluster_ids))
    # print(len(l))
    # permutations = permute(cluster_ids)
    
''' Find all permutations of a cluster list.
'''
def permute(cluster_list):
    permutations = list()
    tmp_list = list()
    backtrack(permutations, tmp_list, cluster_list)
    return permutations

''' Helper function for permutation.
'''
def backtrack(permutations, tmp_list, cluster_list):
    if len(tmp_list) == len(cluster_list):
        permutations.append(list(tmp_list))
        return
    for cluster in cluster_list:
        if cluster in tmp_list:
            continue
        tmp_list.append(cluster)
        backtrack(permutations, tmp_list, cluster_list)
        del tmp_list[len(tmp_list) - 1]

def route_with_sequence(clusters_list):
    cluster_info_dic = cba.get_cluster_adj_dic()
    print(cluster_info_dic)
    road_network_dic, station_info_dic = sp.preprocess()
    stations_shortest_path_dic = sp.get_all_stations_spt_dic_from_file()

    total_time = 0
    average_speed = 3 # m/s
    
    for cluster in clusters_list:
        print("***** cluster", cluster, " *****")
        if cluster == clusters_list[0]:
            path, time = sr.get_visit_path(cluster_info_dic[cluster]['stations'], True)
        else:
            #stat_list = cluster_info_dic[cluster]['stations']
            path, time = sr.get_visit_path(cluster_info_dic[cluster]['stations'], False)
            dist_to_next_cluster, _ = sp.get_shortest_path_from_stat_id(prev_stat, path[0], station_info_dic,
                    stations_shortest_path_dic)
            print("dist_to_next_cluster", dist_to_next_cluster)
            total_time = total_time + (dist_to_next_cluster/average_speed)
        
        print(time)
        print(path)

        prev_stat = path[-1]
        total_time = total_time + time[-1]
        print("total_time", total_time, str(datetime.timedelta(seconds=total_time)))

def get_cluster_permutation(cluster_adj_dic, is_start_fix):
    all_perms = []
    start_stat = '70'
    cur_perm = []
    first = next(iter(cluster_adj_dic))
    
    if is_start_fix:
        first = get_cluster_from_id(start_stat, cluster_adj_dic)
        print("first cluster", first)
    cur_perm.append(first)
    gutil.reset_vertex_visit_dic(cluster_adj_dic)
    dfs_cluster(cur_perm, all_perms, first, cluster_adj_dic)
    #for c in cluster_adj_dic:
    #    dfs_cluster(cur_perm, all_perms, first, cluster_adj_dic)
    
    #print(all_perms)
    perm_len = 0
    perm_cur = []
    for perm in all_perms:
        if len(perm) > perm_len:
            perm_len = len(perm)
            perm_cur = perm
    print(perm_len, perm_cur)
    return all_perms

def get_cluster_from_id(stat_id, cluster_adj_dic):
    for cluster in cluster_adj_dic:
        if stat_id in cluster_adj_dic[cluster]['stations']:
            return cluster
    print("Couldn't find cluster with", stat_id)
    return -1

def dfs_cluster(cur_perm, all_perms, prev, cluster_adj_dic):
    #print(cur_perm)
    found_adj = False
    for cluster in cluster_adj_dic[prev]['adj']:
        if not cluster_adj_dic[cluster]['visited'] and cluster not in cur_perm:
            #print("append", cluster)
            found_adj = True
            cluster_adj_dic[cluster]['visited'] = True
            cur_perm.append(cluster)
            dfs_cluster(cur_perm, all_perms, cluster, cluster_adj_dic)
            del cur_perm[-1]
            cluster_adj_dic[cluster]['visited'] = False
    if not found_adj:
        #print(cur_perm)
        all_perms.append(cur_perm.copy())

if __name__ == '__main__':
    main()
