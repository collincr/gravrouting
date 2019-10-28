import shortest_path as sp

def main():
    road_network_dic, station_info_dic = sp.preprocess()
    stations_shortest_path_dic = sp.get_all_stations_spt_dic_from_file()
    stat1 = 'B-14'
    stat2 = 'B-15'
    if stations_shortest_path_dic is not None:
        distance, path = sp.get_shortest_path(stat1, stat2, station_info_dic,
                stations_shortest_path_dic)
        print('Shortest distance (meter)', distance)
        print('Shortest path', end = ": ")
        for road in path:
            print(road_network_dic[road]['coordinates'], end =", ")
    else:
        print('Please run shortest_path.py to generate the file')

if __name__ == '__main__':
    main()
