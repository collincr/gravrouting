import shortest_path as sp
import cluster_routing as cr
import station_routing as sr
import json
import data_readin_conversion as drc
import pandas as pd
import geopandas as gpd
import os.path

road_network_dic, station_info_dic = sp.preprocess()
cluster_info_dic = cr.get_cluster_info_dic()

local_station_status_csv = '../data/20190829_stn_status.csv'
df_stations = pd.read_csv(local_station_status_csv)
gdf_stations = drc.gdf_constructor(df_stations, 'Easting', 'Northing')
gdf_stations = drc.app_coordinate_converter(gdf_stations)

stat_perm_file = 'stat_perm_cache.json'
stat_perm_with_start_file = 'stat_perm_with_start_cache.json'

def main():

    #print(station_info_dic)
    #print(gdf_stations.loc[0]['geometry'].y)

    stats = ["CSE1", "RE11", "RE34", "RE31", "RE32", "CS19", "CSE5", "RE24", "CS18", "RE25"]
    add_min_perm_with_start_to_cache(stats)

    #make_min_perm_cache()
    #add_min_perm_to_cache(stats)
    #make_new_stat_info()
    #make_new_cluster_info()
    #make_new_time()

def add_min_perm_with_start_to_cache(stations):
    # Assumpt first one is the start
    start = stations[0]
    dic = read_dic_from_file(stat_perm_with_start_file)
    if dic is None:
        print("No file found")
        dic = {}
    key = get_key(stations[1:len(stations)])
    key = start + "#" + key
    if key in dic:
        print("Key " + key + " already in dictionary")
    else:
        min_perm = sr.get_permutation_start_with_station(stations, start)
        dic[key] = {}
        dic[key]["min_permutation"] = min_perm
    print(dic)
    write_dic_to_file(dic, stat_perm_with_start_file)

def make_min_perm_cache():

    cluster_perm_cache = {}
    for c in cluster_info_dic:
        stats = []
        for stat in cluster_info_dic[c]['stations']:
            stats.append(station_info_dic[stat]['name'])

        min_perm = sr.get_permutation_with_mini_time(stats)
        key = get_key(stats)
        #print(stats)
        cluster_perm_cache[key] = {}
        cluster_perm_cache[key]["start"] = min_perm[0]
        cluster_perm_cache[key]["min_permutation"] = min_perm

    write_dic_to_file(cluster_perm_cache, stat_perm_file)

def add_min_perm_to_cache(stations):
    dic = read_dic_from_file(stat_perm_file)
    key = get_key(stations)
    if key in dic:
        print("Key " + key + " already in dictionary")
    else:
        min_perm = sr.get_permutation_with_mini_time(stations)
        dic[key] = {}
        dic[key]['start'] = min_perm[0]
        dic[key]["min_permutation"] = min_perm
    write_dic_to_file(dic, stat_perm_file)

def get_key(stations):
    key = ""
    #print(stations)
    for stat in sorted(stations):
        key = key + stat + "#"
    #print("key:" + key)
    return key

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


        print(cluster_new)
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

def read_dic_from_file(filename):
    filename = '../app_data/' + filename
    if not os.path.exists(filename):
        print(filename, "file not found")
        return None
    with open(filename) as file:
        dic = json.load(file)
    return dic

if __name__ == '__main__':
    main()
