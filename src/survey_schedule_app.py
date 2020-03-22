import shortest_path as sp
import cluster_routing as cr
import json

def main():
    road_network_dic, station_info_dic = sp.preprocess()
    #print(station_info_dic)
    write_dic_to_file(station_info_dic, 'stat_info.json')

    cluster_info_dic = cr.get_cluster_info_dic()
    #print(cluster_info_dic)
    write_dic_to_file(cluster_info_dic, 'cluster_info.json')

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
