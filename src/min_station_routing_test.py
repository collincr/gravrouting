import cluster_routing as cr
import station_routing as sr
import shortest_path as sp
import itertools
import matplotlib.pyplot as plt

from scipy import stats

cluster_info_dic =  None
station_info_dic = None

def main():
    print("main")
    global cluster_info_dic
    global station_info_dic

    cluster_info_dic = cr.get_cluster_info_dic()
    road_network_dic, station_info_dic = sp.preprocess()
    print(cluster_info_dic)
    #print(station_info_dic)
    get_all_stats_travel_time()
    '''
    cluster_id = '1'
    stat_id_list = cluster_info_dic[cluster_id]['stations']
    x, y = get_stats_travel_time(stat_id_list)
    print(len(x), len(y))
    plt.plot(x, y, '.')
    plt.show()
    '''

def get_all_stats_travel_time():
    global cluster_info_dic
    limit = 5
    cluster_id = '1'
    plt.figure(figsize=(12,10))
    #ax = plt.gca()
    plt.plot([], [], '.', label="(P, S, K)")
    for cluster in cluster_info_dic:
        limit = limit - 1
        if limit < 0: 
            break
        
        if 'cluster_id' in locals() and cluster_id != -1:
            limit = 100
            if cluster_id != cluster:
                continue
            else:
                limit = -1
        print("cluster:" + cluster)
        stat_id_list = cluster_info_dic[cluster]['stations']
        if len(stat_id_list) <= 1:
            limit = limit + 1
            continue
        x, y = get_stats_travel_time(stat_id_list)
        r, _ = get_pearson(x, y)
        rho, _ = get_spearman(x, y)
        tau, _ = get_kendalltau(x, y)
        #print(r, p)
        plt.plot(x, y, '.', label="(" + str(round(r, 2)) + ", " + str(round(rho, 2)) + ", " + str(round(tau, 2)) + ")")


    file_name = 'travel_time_comparision_1800_1.png'
    plt.title("Travel time w/o repeat time", fontsize=20)
    plt.xlabel("Travel time without repeat time (s)", fontsize=20)
    plt.ylabel("Travel time with repeat time (s)", fontsize=20)
    plt.legend(loc='lower right')

    plt.savefig(file_name)
    plt.show()

def get_pearson(x, y):
    return stats.pearsonr(x, y)

def get_spearman(x, y):
    return stats.spearmanr(x, y)

def get_kendalltau(x, y):
    return stats.kendalltau(x, y)

def get_stats_travel_time(stat_id_list):
    stat_name_list = stat_id_to_name_list(stat_id_list)
    all_perm = list(itertools.permutations(stat_name_list))
    time_wo_re_list = []
    time_w_re_list = []
    for perm in all_perm:
        #print("perm:", perm)
        travel_time_without_repeat = 0
        travel_time_with_repeat = 0

        # travel time without simulation
        travel_time_without_repeat, perm = sr.add_visit_timestamp(perm)
        #print(travel_time_without_repeat, perm)

        # travel time with simulation (revisit)
        visited_path = []
        visited_time = []
        sr.simulate_visit_station(perm, visited_path, visited_time)
        travel_time_with_repeat = visited_time[-1]
        #print(visited_path)
        #print(visited_time)
        time_wo_re_list.append(travel_time_without_repeat)
        time_w_re_list.append(travel_time_with_repeat)
    return time_wo_re_list, time_w_re_list



def get_key_from_path(stat_path):
    #print("get_key_from_path", stat_path)
    key = ''
    for stat in stat_path:
        key = key + stat + "#"
    return key

def stat_id_to_name_list(stat_id_list):
    stat_name_list = []
    for stat_id in stat_id_list:
        stat_name_list.append(station_info_dic[stat_id]['name'])
    return stat_name_list
    

if __name__ == '__main__':
    main()
