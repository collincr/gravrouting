import cluster_by_agglomerative as cba
import shortest_path as sp
import graph_util as gutil

def main():
    cluster_adj_dic = cba.get_cluster_adj_dic()
    print(len(cluster_adj_dic))
    get_cluster_permutation(cluster_adj_dic, True)
    '''
    perms = []
    dic = {}
    for i in range(0, 20):
        dic[i] = i
    helper([], perms, dic)
    '''
    pass

def route_with_sequence(clusters_list):
    cluster_info_dic = cba.get_cluster_adj_dic()

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
    
    print(all_perms)
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
