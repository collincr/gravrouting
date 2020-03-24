import shortest_path as sp
import cluster_routing as cr
import json

def main():
    road_network_dic, station_info_dic = sp.preprocess()
    #print(station_info_dic)
    stat_info_new = {}
    for stat in station_info_dic:
        name = station_info_dic[stat]['name']
        stat_info_new[name] = {}
        stat_info_new[name]['id'] = stat
        stat_info_new[name]['type'] = station_info_dic[stat]['type']
        stat_info_new[name]['status'] = station_info_dic[stat]['status']
        stat_info_new[name]['coordinates'] = station_info_dic[stat]['coordinates']
        stat_info_new[name]['road_coordinates'] = station_info_dic[stat]['road_coordinates']
        stat_info_new[name]['road_id'] = station_info_dic[stat]['road_id']
    #print(stat_info_new)
    write_dic_to_file(stat_info_new, 'stat_info.json')

    cluster_info_dic = cr.get_cluster_info_dic()
    #print(cluster_info_dic)
    cluster_new = {}
    for c in cluster_info_dic:
        cluster_new[c] = {}
        stats = []
        for stat in cluster_info_dic[c]['stations']:
            stats.append(station_info_dic[stat]['name'])
        cluster_new[c]['stations'] = stats
        cluster_new[c]['adj'] = cluster_info_dic[c]['adj']
    print(cluster_new)
    write_dic_to_file(cluster_new, 'cluster_info.json')


    stat_times_dic = json.load(open("time.json"))
    #print(stat_times_dic)
    new_time_dic = {}
    for start in stat_times_dic:
        new_time_dic[start] = {}
        for end in stat_times_dic[start]:
            #print(stat_times_dic[start][end])
            new_time_dic[start][end] = round(stat_times_dic[start][end])
    #print(new_time_dic)
    write_dic_to_file(new_time_dic, 'stat_travel_time.json')

def write_dic_to_file(dic, filename):
    filepath = '../app_data/' + filename
    with open(filepath, 'w') as outfile:
        json.dump(dic, outfile)


if __name__ == '__main__':
    main()
