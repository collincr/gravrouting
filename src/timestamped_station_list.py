import datetime as dt
from shortest_path import internal_get_spt_from_stat_name

STATIONS = [
    ["ZAP28", "RE16", "CS15", "JOSRIDGE", "J214", "CS14", "VOLPK"],
    ["B-15", "DOR64", "DOR65", "DOR66", "CS1", "B-14", "DOR68"],
    ["CS25", "CS26", "COSO2", "CS44", "CS43"],
    ["CS28", "J217", "CS29", "CS52", "CS30", "J4", "CS41"],
    ["CS12", "CS36", "CS37", "CS13", "CS38", "CS64", "CS63"],
    ["CS7", "CS3", "CS6", "CS4", "HW4", "CS5", "CS65"],
    ["CS8", "DOR37", "DOR38", "DOR39", "CS34", "CS35", "CS9"],
    ["DOR68", "CS20", "ZAP29", "RE15", "RE12", "RE14", "CS17"],
    ["RE13", "RE11", "RE34", "CS19", "CSE5", "CS18", "RE25"],
    ["COSO3", "RE40", "RE39", "CS31", "RE2", "RE35"],
    ["SLME", "RE7", "RE5", "CER15", "CSE1", "RE8", "ZAP15"],
    ["RE32", "RE31", "CSE3", "RE30", "CS70", "RE27A", "CSE4"],
    ["RE5", "CER15", "CSE1", "RE4", "CER1", "DOR72", "RE36"]
]


def main():
    timestamped_station(2)


''' Given an index to get a list of station in STATIONS.
    Show timestamps for each station of all permuations.
    Return the station permutation with shortest time consumed. 
'''
def timestamped_station(index):    
    station_list = STATIONS[index]
    permutations = permute(station_list)
    count = 1
    min_time = float("inf")
    shortest = None
    for stations in permutations:
        res, total_time = add_visit_timestamp(stations)
        if total_time < min_time:
            min_time = total_time
            shortest = stations
        print("Departure and arrival time of each station")
        print("Situation [" + str(count) + "]")
        print(res)
        count += 1

    return shortest

''' Find all permutations of a station list.
'''
def permute(station_list):
    permutations = list()
    tmp_list = list()
    backtrack(permutations, tmp_list, station_list)
    return permutations


''' Helper function for permutation.
'''
def backtrack(permutations, tmp_list, station_list):
    if len(tmp_list) == len(station_list):
        permutations.append(list(tmp_list))
        return
    for station in station_list:
        if station in tmp_list:
            continue
        tmp_list.append(station)
        backtrack(permutations, tmp_list, station_list)
        del tmp_list[len(tmp_list) - 1]


''' Add time for each station in the list.
    All times are measured in secondes.
'''
def add_visit_timestamp(stations):
    last_station = None
    res = list()

    for station in stations:

        if last_station == None:
            arrival_time = 0
        else:
            # 3m/s i.e. 10.8km/h Average speed on unpaved road
            speed = 3
            _, distance = internal_get_spt_from_stat_name(last_station, station)
            road_time = distance // speed   # intra-station time (secs)
            arrival_time = departure_time + road_time

        measure_time = 150                  # inner-station time (secs)
        departure_time = arrival_time + measure_time
        last_station = station

        entry = station + ", " + str(dt.timedelta(seconds = arrival_time)) \
                + ", " + str(dt.timedelta(seconds = departure_time))
        res.append(entry)

    return res, departure_time


if __name__ == '__main__':
    main()