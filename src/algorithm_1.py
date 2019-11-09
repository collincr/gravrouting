import datetime as dt
import collections
import operator
import time
from shortest_path import internal_get_spt_from_stat_name
import shortest_path as sp

distance_dct = {}
road_network_dic = None
station_info_dic = None
stations_shortest_path_dic = None
'''
def main():
	print(str(dt.timedelta(seconds = time.time())))
	# Initialize the station dict
	road_network_dic, station_info_dic = sp.preprocess()
	stations_shortest_path_dic = sp.get_all_stations_spt_dic_from_file()

	station_list = {"B-15", "DOR64", "DOR65", "DOR66", "CS1", "B-14", "DOR68"}
	permutation_list = get_permutation_with_mini_time(station_list)
	#permutation_list = ['CS44', 'COSO2', 'CS43', 'CS25', 'CS26']
	print("first permutation:")
	print(permutation_list)
	simulate_visit_station(permutation_list)
	print(str(dt.timedelta(seconds = time.time())))
'''
def main():
    '''
    station_list = {"B-15", "DOR64", "DOR65", "DOR66", "CS1", "B-14", "DOR68"}
    #print(station_list)

    stat_dic = sp.get_station_dic()
    stat_name_dic = sp.create_stat_name_id_mapping(stat_dic)
    for stat in station_list:
        print(stat, stat_name_dic[stat])
    '''
    stat_id_list = {'6', '37', '38', '39', '47', '4', '40'}
    time, visit_path = get_visit_path(stat_id_list)

def get_visit_path(stat_id_list):

    print(str(dt.timedelta(seconds = time.time())))
    # Initialize the station dict
    road_network_dic, station_info_dic = sp.preprocess()
    stations_shortest_path_dic = sp.get_all_stations_spt_dic_from_file()

    station_list = []
    for stat_id in stat_id_list:
        station_list.append(str(station_info_dic[stat_id]['name']))

    #print(station_list)
    permutation_list = get_permutation_with_mini_time(station_list)
    print("first permutation:")
    print(permutation_list)
    visit_time, visit_path = simulate_visit_station(permutation_list)
    print(str(dt.timedelta(seconds = time.time())))

    return visit_time, visit_path

def getTime(timestr):
	minute = timestr / 60
	second = (timestr % 60) * 60
	return str(minute) + ":" + str(second)
	
def getDistance(station1, station2):
	if station1 in distance_dct and station2 in distance_dct[station1]:
		#print("cache")
		return None, distance_dct[station1][station2]

	if station2 in distance_dct and station1 in distance_dct[station2]:
		#print("cache")
		return None, distance_dct[station2][station1]
	
	distance = 0
	if stations_shortest_path_dic is not None:
		distance, path = sp.get_shortest_path(station1, station2, station_info_dic,
				stations_shortest_path_dic)
	else:
		_, distance = internal_get_spt_from_stat_name(station1, station2)

	if station1 not in distance_dct:
		distance_dct[station1] = {}
	
	distance_dct[station1][station2] = distance
	return None, distance
	

def get_permutation_with_mini_time(station_list):
	permutations = permute(station_list)
	min_time = 0
	permutation_list = []
	for stations in permutations:
		time, res = add_visit_timestamp(stations)
		if min_time == 0 or time < min_time:
			min_time = time
			permutation_list = res
	print("get_permutation_with_mini_time")
	print(permutation_list)
	print(min_time)
	return permutation_list
	
def get_permutation_start_with_station(station_list, station):
	permutations = permute(station_list)
	min_time = 0
	permutation_list = []
	for stations in permutations:
		if not stations[0] == station:
			continue
		time, res = add_visit_timestamp(stations)
		if min_time == 0 or time < min_time:
			min_time = time
			permutation_list = res
	print("get_permutation_start_with_station")
	print(permutation_list)
	return permutation_list

def simulate_visit_station(permutation_list):
	N = 1800
	M = 900
	test_time = 150
	speed = 3
	last_time_repeat = 0
	current_time = 0
	visited_stations = []
	visit_path = []
	visit_time = []
	index = 0
	left_stations = permutation_list
	previous_time = 0
	current_station = left_stations[0]
	
	while len(left_stations) > 0:
		if current_station in left_stations:
			left_stations.remove(current_station)
		
		print("visit: "+str(current_station)+" at time: "+getTime(current_time))
		visit_path.append(current_station)
		visit_time.append(current_time)
		
		# Simulate the test time
		current_time = current_time + test_time

		if current_time - last_time_repeat > N:
			print("Making choice!!!!!!!")
			print(current_station)
			if len(visit_path) == 0:
				print("Error!!!!!!!!!!!!!!!!!!!!!!!!!")
			else:
				station_travel_time = {}
				for i in range(0, len(visit_path)):
					_, distance = getDistance(current_station, visit_path[i])
					print(visit_path[i])
					travel_time = distance // speed
					print(getTime(travel_time))
					if current_time - visit_time[i] + travel_time > N and travel_time < M:
						station_travel_time[visit_path[i]] = travel_time
				# Choose the station with minimum travel time
				if len(station_travel_time) > 0:
					sorted_s = sorted(station_travel_time.items(), key=operator.itemgetter(1))
					sorted_station = collections.OrderedDict(sorted_s)
					first_station = next(iter(sorted_station))
					
					# Go back to visit the repeat station
					current_station = first_station
					current_time += station_travel_time[first_station]
					last_time_repeat = current_time
					
					# Update the new order
					new_list = []
					new_list.append(current_station)
					for station in left_stations:
						new_list.append(station)
					left_stations = get_permutation_start_with_station(new_list, current_station)
					left_stations.remove(current_station)
					continue
				else:
					print("No visited stations satisfy the repeat condition!!!!!!")

		if len(left_stations) > 0:
			next_station = left_stations[0]
			_, distance = getDistance(current_station, next_station)
			travel_time = distance // speed
			current_time += travel_time
			current_station = next_station
	
	print("final path:")
	print(visit_path)
	print(visit_time)
	return visit_path, visit_time


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
	departure_time = 0
	for station in stations:

		if last_station == None:
			arrival_time = 0
		else:
			# 10m/s i.e. 36km/h Will be speed between actual station
			speed = 10
			_, distance = getDistance(last_station, station)
			road_time = distance // speed   # intra-station time (secs)
			arrival_time = departure_time + road_time

		measure_time = 150                  # inner-station time (secs)
		departure_time = arrival_time + measure_time
		last_station = station

		res.append(station)

	return departure_time, res


if __name__ == '__main__':
	main()