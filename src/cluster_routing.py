import cluster_by_agglomerative as cba
import shortest_path as sp
import graph_util as gutil
import station_routing as sr
import datetime
import datetime as dt
import time
import itertools
import files
import numpy as np
import os.path
import json
import cluster_w_merge as cm

from heapq import heappush, heappop

road_network_dic, station_info_dic = sp.preprocess()
stat_name_dic = sp.create_stat_name_id_mapping(station_info_dic)
cluster_info_dic =  None

def main():
    #global cluster_info_dic
    #cluster_info_dic = read_cluster_dic_from_file()
    #print(str(dt.timedelta(seconds = time.time())))
    #cluster_adj_dic = cba.get_cluster_adj_dic()
    #print(cluster_adj_dic)
    #get_cluster_permutation(cluster_adj_dic, True)
    #cluster_seq = ['0', '8', '14', '13', '12', '5', '15', '11', '6', '7', '10',
    #        '9', '17', '1', '2', '3', '4', '18', '19', '16']
    #route_with_sequence(cluster_seq, cl, cluster_adj_dic)
    # get_cluster_permutations(cluster_adj_dic)
    #print(str(dt.timedelta(seconds = time.time())))

    #perms = []
    #dic = {}
    #for i in range(0, 20):
    #    dic[i] = i
    #helper([], perms, dic)
    #write_cluster_dic_to_file(cba.get_cluster_adj_dic())
    #t1 = time.time()
    #greedy_routing(8*60*60)
    #t2 = time.time()
    #print("time to run greedy", t2-t1, str(datetime.timedelta(seconds=t2-t1)))

    #get_start_stat_dic(cluster_adj_dic)
    #print(cluster_adj_dic)
    #write_cluster_dic_to_file(cluster_adj_dic)
    #cluster_info_dic = read_cluster_dic_from_file()
    #print(cluster_info_dic)

    #agg_cluster_dic = cm.get_agg_cluster_dic()
    #get_start_stat_dic(agg_cluster_dic)
    #write_cluster_dic_to_file(agg_cluster_dic, './agg_cluster_dic.json')
    agg_cluster_dic = read_cluster_dic_from_file(files.agg_cluster_dic_json)
    print(agg_cluster_dic)
    t1 = time.time()
    greedy_routing_cut_cluster(agg_cluster_dic, 8*60*60)
    t2 = time.time()
    print("time to run greedy", t2-t1, str(datetime.timedelta(seconds=t2-t1)))

    #cluster_adj_dic = cba.get_cluster_adj_dic()
    #get_next_day_station_seq(cluster_adj_dic)
    #print(len(agg_cluster_dic))
    pass
'''
def calculate_route_for_all_clusters():
    cluster_adj_dic = cba.get_cluster_adj_dic()
    for c in cluster_adj_dic:
        stat_list = cluster_adj_dic[c]['stations']
'''

def preprocess_cluster():
    global cluster_info_dic
    if cluster_info_dic is None:
        cluster_info_dic = read_cluster_dic_from_file()
    if cluster_info_dic is None:
        cluster_adj_dic = cba.get_cluster_adj_dic()
        get_start_stat_dic(cluster_adj_dic)
        write_cluster_dic_to_file(cluster_adj_dic, files.clusters_info_json)
        cluster_info_dic = cluster_adj_dic
    return cluster_info_dic

def get_next_day_station_seq(cluster_dic):
    global station_info_dic
    get_start_stat_dic(cluster_dic)
    stations_route = greedy_routing_cut_cluster(cluster_dic, 8*60*60)
    stations_everyday = {}
    for day in stations_route:
        stats = stations_route[day]['path']
        stations_everyday[day] = [station_info_dic[i]['name'] for i in stats]

    print(stations_everyday)
    return stations_everyday

def greedy_routing_cut_cluster(cluster_info_dic, time_limit):

    #preprocess_cluster()

    #global cluster_info_dic
    global station_info_dic
    global stat_name_dic
    gutil.reset_vertex_visit_dic(cluster_info_dic)
    stat_sp_dic = sp.get_all_stations_spt_dic_from_file()

    visited_path = []
    visited_timestamp = []
    start_stat = '70'
    prev_stat = start_stat
    total_time = 0

    remove_stat_from_cluster(start_stat, cluster_info_dic)
    visited_path.append(prev_stat)
    visited_timestamp.append(0)
    prev_len = len(visited_path)

    cluster_id_start = 100
    day = 0
    visited_clusters = [[]]
    station_route = {}

    #print(cluster_info_dic)
    print("cluster count:", len(cluster_info_dic))
    while not all_clusters_visited(cluster_info_dic):
        # find closest cluster
        next_cluster = -1
        min_time = np.Inf
        for c in cluster_info_dic:
            if not cluster_info_dic[c]['visited']:
                cur_time = sr.get_travel_time_from_id(prev_stat, cluster_info_dic[c]['start'])
                if cur_time < min_time:
                    min_time = cur_time
                    next_cluster = c

        if next_cluster == -1:
            print("Something wrong about finding next cluster")
            break

        print("***** Go to cluster", next_cluster, " *****", cluster_info_dic[next_cluster]['stations'])
        visited_path, visited_timestamp = sr.get_visit_path_by_id(
                cluster_info_dic[next_cluster]['stations'],
                visited_path, visited_timestamp)
        visited_clusters[day].append(next_cluster)
        print(visited_path)
        print(visited_timestamp)

        # Set visited for the cluster
        cluster_info_dic[next_cluster]['visited'] = True
        prev_stat = visited_path[-1]

        # Check if we can finish the cluster
        last_idx = len(visited_path)-1
        last_stat = visited_path[last_idx]
        total_time = visited_timestamp[last_idx] + sr.get_travel_time_from_id(last_stat, start_stat)
        finish_today = False
        if total_time > time_limit:
            print("Exceed time limit")
            finish_today = True
            while total_time > time_limit:
                #print("last_stat:", visited_path[last_idx], visited_timestamp[last_idx])
                #print("Time back:", sr.get_travel_time_from_id(last_stat, start_stat))
                last_idx = last_idx - 1
                last_stat = visited_path[last_idx]
                total_time = visited_timestamp[last_idx] + sr.get_travel_time_from_id(last_stat, start_stat)

            print("last_stat:", visited_path[last_idx], visited_timestamp[last_idx])
            print("Time back:", sr.get_travel_time_from_id(last_stat, start_stat))
            # Create new cluster
            remain_stats = set()
            for i in range(last_idx + 1, len(visited_path)):
                if visited_path[i] in cluster_info_dic[next_cluster]['stations']:
                    remain_stats.add(visited_path[i])
            print("remain_stats", remain_stats)
            c_id = str(cluster_id_start)
            cluster_id_start = cluster_id_start + 1
            cluster_info_dic[c_id] = {}
            cluster_info_dic[c_id]['visited'] = False
            cluster_info_dic[c_id]['stations'] = list(remain_stats)
            cluster_info_dic[c_id]['start'] = get_start_stat_of_cluster(cluster_info_dic[c_id]['stations'])

        if all_clusters_visited(cluster_info_dic):
            finish_today = True

        if finish_today:
            # Finish this day
            print("----- Finish day", day, " -----")
            prev_stat = start_stat
            station_route[day] = {}
            station_route[day]['total_time'] = int(total_time)
            station_route[day]['path'] = visited_path[0:last_idx+1]
            station_route[day]['timestamp'] = [ int(t) for t in visited_timestamp[0:last_idx+1] ]

            visited_path = []
            visited_timestamp = []
            day = day + 1
            total_time = 0
            visited_clusters.append([])
            finish_today = False

        print("final path", visited_path)
        print("final time", visited_timestamp)

    del visited_clusters[-1]
    print("final cluster:", cluster_info_dic)
    print("visited_clusters", visited_clusters)
    print("station_route", station_route)
    return station_route

def greedy_routing(time_limit):
    global station_info_dic
    cluster_adj_dic = cba.get_cluster_adj_dic()
    gutil.reset_vertex_visit_dic(cluster_adj_dic)
    #road_network_dic, station_info_dic = sp.preprocess()
    stat_sp_dic = sp.get_all_stations_spt_dic_from_file()

    visited_path = []
    visited_timestamp = []
    prev_stat = '70'
    total_time = 0
    avg_speed = 3

    remove_stat_from_cluster(prev_stat, cluster_adj_dic)
    visited_path.append(prev_stat)
    visited_timestamp.append(0)
    prev_len = len(visited_path)

    day = 0
    cluster_visited = [[]]
    station_route = {}

    while not all_clusters_visited(cluster_adj_dic):
        cluster_cand_pq = get_cluster_cands(prev_stat, cluster_adj_dic, visited_path, visited_timestamp)

        found_next = False
        tmp_list = []
        #cand_time = -1
        time_to_cand = np.Inf
        cand_cluster = -1
        cand_path = []
        cand_timestamp = []

        while not found_next:
            time_to_cand, cand_cluster, cand_path, cand_timestamp = heappop(cluster_cand_pq)
            time_to_finish_cand = cand_timestamp[-1] - cand_timestamp[prev_len-1]
            if total_time +  time_to_finish_cand > time_limit:
                tmp_list.append((time_to_cand, cand_cluster, cand_path, cand_timestamp))
            else:
                found_next = True
                print("Found", cand_cluster, time_to_cand)

            if len(cluster_cand_pq) == 0:
                break

        for item in tmp_list:
            heappush(cluster_cand_pq, item)

        if found_next:
            #print("***** Go to cluster", cand_cluster, "***** before:", total_time)
            print("***** Go to cluster", cand_cluster, "***** before:", visited_path)
            print("***** Go to cluster", cand_cluster, "***** before:", visited_timestamp)
            total_time = total_time + time_to_finish_cand
            visited_path = cand_path
            visited_timestamp = cand_timestamp
            cluster_adj_dic[cand_cluster]['visited'] = True
            station_route[cand_cluster] = cand_path[prev_len:]
            prev_len = len(visited_path)
            prev_stat = visited_path[-1]

            cluster_visited[day].append(cand_cluster)

            print("***** Go to cluster", cand_cluster, "***** after:", total_time)
            print("***** Go to cluster", cand_cluster, "***** after:", visited_path)
            print("***** Go to cluster", cand_cluster, "***** after:", visited_timestamp)
        else: # leave it tomorrow
            print("Finish this day", total_time)
            visited_path = []
            visited_timestamp = []
            total_time = 0
            #time_limit = 0
            prev_stat = '70'

            visited_path.append(prev_stat)
            visited_timestamp.append(0)
            prev_len = len(visited_path)

            day = day + 1
            cluster_visited.append([])
        #prev_stat = visited_stat[-1]
        #prev_len = len(visited_time)

        #dist_to_next_cluster,_ = sp.get_shortest_path_from_stat_id(prev_stat, next_stat,
        #        station_info_dic, stat_sp_dic)
        #time_to_next_cluster = dist_to_next_cluster/avg_speed +

        #total_time = total_time + dist_to_next_cluster/avg_speed
        #total_time = total_time + (visited_time[-1] - visited_time[prev_len-1])

    print("cluster_visited:", cluster_visited)
    print("station route", station_route)

def get_cluster_cands(stat, cluster_dic, visited_stat, visited_time):
    print("get_cluster_cands")
    global station_info_dic
    #road_network_dic, station_info_dic = sp.preprocess()
    stat_sp_dic = sp.get_all_stations_spt_dic_from_file()
    #avg_speed = 3
    cur_len = len(visited_stat)
    '''
    min_time = np.Inf
    min_visited_path = []
    min_visited_time = []
    min_cluster = -1
    '''
    pq = []
    print("current visited_stat", visited_stat)
    print("current visited_time", visited_time)

    for c in cluster_dic:
        if cluster_dic[c]['visited']:
            continue

        print("--- check cluster", c, "---")
        path, time = sr.get_visit_path_by_id(cluster_dic[c]['stations'],
                visited_stat.copy(), visited_time.copy())
        print("path with cluster", c, path)
        print("time with cluster", c, time)
        #print("cur_len", cur_len)

        #dist, _ = sp.get_shortest_path_from_stat_id(stat, path[cur_len],
                #station_info_dic,stat_sp_dic)
        #time_to_c = dist/avg_speed
        time_to_c = sr.getTravelTime(station_info_dic[stat]['name'], station_info_dic[path[cur_len]]['name'])
        print("time_to_c with cluster", c, time_to_c)
        #travel_time = time[-1]  # time?
        #travel_time = time_to_c + (time[-1] - visited_time[cur_len-1]) # time?
        '''
        if travel_time < min_time:
            min_time = travel_time
            min_visited_path = path
            min_visted_time = time
            min_cluster = c
        '''
        heappush(pq, (time_to_c, c, path, time,))
    '''
    for i in range(cur_len, min_visited_path):
        visited_stat.append(min_visited_path[i])
        visited_time.append(min_visited_time[i])
    '''
    return pq

def get_start_stat_dic(cluster_dic):
    for c in cluster_dic:
        stats = cluster_dic[c]['stations']
        cluster_dic[c]['start'] = get_start_stat_of_cluster(stats)
        print("cluster", c, "start with", cluster_dic[c]['start'])

def get_start_stat_of_cluster(stat_id_list):
    #print("get_start_stat_of_cluster", stat_id_list)
    global station_info_dic
    global stat_name_dic
    stat_name_list = []
    for stat in stat_id_list:
        stat_name_list.append(station_info_dic[stat]['name'])
    min_time_route = sr.get_permutation_with_mini_time(stat_name_list)
    return stat_name_dic[min_time_route[0]]

def all_clusters_visited(cluster_dic):
    for c in cluster_dic:
        if not cluster_dic[c]['visited']:
            return False
    print("All clusters visited")
    return True

def remove_stat_from_cluster(stat, cluster_dic):
    for c in cluster_dic:
        if stat in cluster_dic[c]['stations']:
            cluster_dic[c]['stations'].remove(stat)

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

def route_with_sequence(clusters_list, cluster_info_dic):

    #print(cluster_info_dic)
    road_network_dic, station_info_dic = sp.preprocess()
    stations_shortest_path_dic = sp.get_all_stations_spt_dic_from_file()
    
    stat_name_dic = sp.create_stat_name_id_mapping(station_info_dic)
    
    total_time = 0
    average_speed = 3 # m/s
    visit_path = []
    visit_time = []
    total_time_list = []
    for cluster in clusters_list:
        print("***** cluster", cluster, " *****")
        path, time = sr.get_visit_path(cluster_info_dic[cluster]['stations'], visit_path, visit_time)
        if cluster != clusters_list[0]:
            dist_to_next_cluster, _ = sp.get_shortest_path_from_stat_id(prev_stat, stat_name_dic[path[0]], station_info_dic,stations_shortest_path_dic)
            print("dist_to_next_cluster", dist_to_next_cluster)
            total_time = total_time + (dist_to_next_cluster/average_speed)
        
        print(time)
        print(path)

        prev_stat = stat_name_dic[path[-1]]
        total_time = time[-1]
        print("total_time", total_time, str(datetime.timedelta(seconds=total_time)))
        total_time_list.append(total_time)
    return total_time_list

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

def write_cluster_dic_to_file(cluster_dic, filename):
    for cluster in cluster_dic:
        stats = cluster_dic[cluster]['stations']
        if isinstance(stats, np.ndarray):
            cluster_dic[cluster]['stations'] = cluster_dic[cluster]['stations'].tolist()
        cluster_dic[cluster]['adj'] = list(cluster_dic[cluster]['adj'])
    gutil.write_dic_to_json(cluster_dic, filename)

def read_cluster_dic_from_file(filename):
    if not os.path.exists(filename):
        print(filename, "file not found")
        return None
    with open(filename) as file:
        dic = json.load(file)
    return dic

if __name__ == '__main__':
    main()
