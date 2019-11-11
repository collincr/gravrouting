import numpy as np
import shortest_path as sp
import matplotlib.pyplot as plt
import geopandas as gpd
import files
import time

from sklearn.cluster import AgglomerativeClustering

cluster_stat_dic = {}
label = 0
cluster_size_limit = 13
recluster_num = 3
cluster_num = 9
stat_list = None
dist_matrix = None

def main():
    #t1 = time.time()
    cluster_stat_dic = get_cluster_dic()
    #t2 = time.time()
    #print('get_cluster_dic took', t2-t1)

    find_cluster_adj(cluster_stat_dic)
    #t3 = time.time()
    #print('find_cluster_adj took', t3-t2)
    #plot_clustering_from_dic(cluster_stat_dic)
    pass

def get_cluster_adj_dic():
    return find_cluster_adj(get_cluster_dic())

def get_cluster_dic():
    global stat_list
    global dist_matrix
    station_dic = sp.get_station_dic()
    dist_matrix = compute_dis_matrix()

    stat_list = np.array(list(station_dic.keys()))
    
    cluster_labels = agglomerative_clustering(cluster_num, dist_matrix)

#    cluster_stat_dic = {}
#    for i in range(0, cluster_number):
#        cluster_stat_dic[str(i)] = {}
#        cluster_stat_dic[str(i)]['stations'] = stat_list[cluster_labels==i]

    #print(cluster_stat_dic)
    #print(cluster_stat_dic['0'])
    #print(cluster_stat_dic)
    return cluster_stat_dic

def reCluster(dirmap):
    # Re-cluster
    global label
    dis_metrix = [([0] * len(dirmap)) for i in range(len(dirmap))]
    for station in range(0,len(dirmap)):
        for station1 in range(0,len(dirmap)):
            if station != station1:
                dis_metrix[station][station1] = dist_matrix[dirmap[station]][dirmap[station1]]
                dis_metrix[station1][station] = dist_matrix[dirmap[station]][dirmap[station1]]
    
    recluster_num = int(len(dirmap) / 7)
    hc2 = AgglomerativeClustering(n_clusters=recluster_num, affinity = 'precomputed', linkage = 'average')
    dis_metrix = np.array(dis_metrix)
    y_hc2 = hc2.fit_predict(dis_metrix)
    
    number = 1
    for sub2 in range(0,recluster_num):
        num = 0
        if np.count_nonzero(y_hc2 == sub2) > cluster_size_limit:
            dirmap2 = {}
            index = 0
            for i in range(0, len(y_hc2)):
                if sub2 == y_hc2[i]:
                    dirmap2[index] = dirmap[i]
                    index += 1
            reCluster(dirmap2)
        else:
            cluster_stat_dic[str(label)] = {}
            cluster_stat_dic[str(label)]['stations'] = []
            for i in range(0, len(y_hc2)):
                if sub2 == y_hc2[i]:
                    num += 1
                    cluster_stat_dic[str(label)]['stations'].append(stat_list[dirmap[i]])
            cluster_stat_dic[str(label)]['stations'] = np.array(cluster_stat_dic[str(label)]['stations'])
            label += 1

def find_cluster_adj(cluster_stat_dic):
    stat_adj_dic = sp.get_station_adj_dic()
    for c1 in cluster_stat_dic:
        cluster_stat_dic[c1]['adj'] = set()
        for c2 in cluster_stat_dic:
            if c1 != c2:
                #print("Check clusters", c1, c2)
                if is_cluster_adj(cluster_stat_dic[c1]['stations'],
                        cluster_stat_dic[c2]['stations'], stat_adj_dic):
                    cluster_stat_dic[c1]['adj'].add(c2)
    #print(cluster_stat_dic)
    return cluster_stat_dic

def plot_clustering_from_dic(cluster_stat_dic):
    stat_info_dic = sp.get_station_dic()
    plt.rcParams['figure.figsize'] = (12, 9)
    df_roads = gpd.read_file(files.roads_pads_network_utm_geojson)
    df_roads.plot(color='black')

    for cluster in cluster_stat_dic:
        stats = cluster_stat_dic[cluster]['stations']
        stat_coords  = []

        # plot stations
        for stat in stats:
            stat_coords.append(stat_info_dic[stat]['coordinates'])
        stat_coords = np.array(stat_coords)
        plt.scatter(stat_coords[:, 0], stat_coords[:, 1])

        # plot annotate
        if False:
            for stat in stats:
                e = stat_info_dic[stat]['coordinates'][0]
                n = stat_info_dic[stat]['coordinates'][1]
                plt.annotate(stat, xy=(e, n), xytext=(e+10, n+10))

        if True:
            for coord in stat_coords:
                plt.annotate(cluster, xy=(coord[0], coord[1]), xytext=(coord[0]+10,
                    coord[1]+10))
    plt.title('Stations with ' +  str(len(cluster_stat_dic)) + ' clusters')
    plt.xlabel('Easting [m]', fontsize=13)
    plt.ylabel('Northing [m]', fontsize=13)
    filename = '../resources/img/stations_clustering.png'
    #plt.savefig(filename, dpi=1000)
    #plt.show()

def is_cluster_adj(cluster1_stats, cluster2_stats, stat_adj_dic):
    for stat1 in cluster1_stats:
        for stat2 in cluster2_stats:
            if stat1 == stat2:
                print("stat1 and stat2 should not be the same!", stat1, stat2)
            else:
                if stat1 not in stat_adj_dic:
                    print("Couldn't find stat1", stat1, "in stat_adj_dic")
                else:
                    if stat2 in stat_adj_dic[stat1]['adj']:
                        return True
    return False

def agglomerative_clustering(cluster_num, dist_matrix):
    global label
    hc = AgglomerativeClustering(n_clusters=cluster_num, affinity = 'precomputed',
            linkage = 'average')
    y_hc = hc.fit_predict(dist_matrix)
    
    for sub in range(0,cluster_num):
        x = stat_list[y_hc ==sub]
        num = 0
        if len(x) > cluster_size_limit:
            dirmap = {}
            index = 0
            for i in range(0, len(y_hc)):
                if y_hc[i] == sub:
                    dirmap[index] = i
                    index += 1
            reCluster(dirmap)
        else:
            cluster_stat_dic[str(label)] = {}
            cluster_stat_dic[str(label)]['stations'] = stat_list[y_hc==sub]
            label += 1
    
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
