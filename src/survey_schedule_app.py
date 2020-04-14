import shortest_path as sp
import cluster_routing as cr
import station_routing as sr
import json
import data_readin_conversion as drc
import pandas as pd
import geopandas as gpd

road_network_dic, station_info_dic = sp.preprocess()
cluster_info_dic = cr.get_cluster_info_dic()

local_station_status_csv = '../data/20190829_stn_status.csv'
df_stations = pd.read_csv(local_station_status_csv)
gdf_stations = drc.gdf_constructor(df_stations, 'Easting', 'Northing')
gdf_stations = drc.app_coordinate_converter(gdf_stations)

def main():

    #print(station_info_dic)
    #print(gdf_stations.loc[0]['geometry'].y)

    make_new_stat_info()
    make_new_cluster_info()
    make_new_time()

def make_new_stat_info():
        stat_info_new = {}
        for stat in station_info_dic:
            name = station_info_dic[stat]['name']
            stat_info_new[name] = {}
            stat_info_new[name]['id'] = stat
            stat_info_new[name]['cluster'] = get_cluster(stat, cluster_info_dic)

            found_coord = False
            for i in range(len(gdf_stations)) :
                if gdf_stations.loc[i, "StationName"] == name:
                    if found_coord:
                        print("Found second coordinates of " + name)
                    found_coord = True
                    point = gdf_stations.loc[i, "geometry"]
                    stat_info_new[name]["coordinates"] = [point.y, point.x]
            if not found_coord:
                print("Coordinates not found for " + name)
            #stat_info_new[name]['type'] = station_info_dic[stat]['type']
            #stat_info_new[name]['status'] = station_info_dic[stat]['status']
            #stat_info_new[name]['coordinates'] = station_info_dic[stat]['coordinates']
            #stat_info_new[name]['road_coordinates'] = station_info_dic[stat]['road_coordinates']
            #stat_info_new[name]['road_id'] = station_info_dic[stat]['road_id']
        #print(stat_info_new)
        write_dic_to_file(stat_info_new, 'stat_info.json')

def make_new_cluster_info():
        #print(cluster_info_dic)
        cluster_new = {}
        cluster_perm_cache = {}
        for c in cluster_info_dic:
            cluster_new[c] = {}
            stats = []
            for stat in cluster_info_dic[c]['stations']:
                stats.append(station_info_dic[stat]['name'])
            #cluster_new[c]['adj'] = cluster_info_dic[c]['adj']
            min_perm = sr.get_permutation_with_mini_time(stats)
            cluster_new[c]['start'] = min_perm[0]
            cluster_new[c]['stations'] = stats
            #cluster_new[c]['min_permutation'] = min_perm
            #path, time = sr.get_visit_path_by_name(stats, [], [])
            #cluster_new[c]['visit_path'] = path
            #cluster_new[c]['visit_time'] = time

            # cluster start cache
            key = ""
            #print(stats)
            for stat in sorted(stats):
                key = key + stat + "#"
            print("key:" + key)
            cluster_perm_cache[key] = {}
            cluster_perm_cache[key]["min_permutation"] = min_perm
            cluster_perm_cache[key]["start"] = min_perm[0]

        print(cluster_new)
        write_dic_to_file(cluster_perm_cache, 'stat_perm_cache.json')
        write_dic_to_file(cluster_new, 'cluster_info.json')

def make_new_time():
        stat_times_dic = json.load(open("time.json"))
        #print(stat_times_dic["DOR37"])
        #print(stat_times_dic)
        new_time_dic = {}
        for start in stat_times_dic:
            new_time_dic[start] = {}
            for end in stat_times_dic[start]:
                #print(stat_times_dic[start][end])
                new_time_dic[start][end] = round(stat_times_dic[start][end])
        print(new_time_dic["DOR37"]["DOR38"])
        write_dic_to_file(new_time_dic, 'stat_travel_time.json')

def get_cluster(stat_id, cluster_info_dic):
    for cluster in cluster_info_dic:
        if stat_id in cluster_info_dic[cluster]['stations']:
            return cluster
    print("Couldn't find station in clusters")
    return -1

def write_dic_to_file(dic, filename):
    filepath = '../app_data/' + filename
    with open(filepath, 'w') as outfile:
        json.dump(dic, outfile)


if __name__ == '__main__':
    main()
