import shortest_path as sp
import cluster_by_agglomerative as cba
import json
import operator
import collections
import itertools

N = 1800
M = 900
distance_dct = {}

def main():
	station_sequence = ["B-15", "DOR64", "DOR65", "DOR66", "CS1", "B-14", "DOR68"]
	stations_everyday = {'1':[["ZAP28", "RE16", "CS15", "JOSRIDGE", "J214", "CS14", "VOLPK"], ["B-15", "DOR64", "DOR65", "DOR66", "CS1", "B-14", "DOR68"]], '2':[["CS28", "J217", "CS29", "CS52", "CS30", "J4", "CS41"], ["CS12", "CS36", "CS37", "CS13", "CS38", "CS64", "CS63"]], '3':[["CS7", "CS3", "CS6", "CS4", "HW4", "CS5", "CS65"], ["CS8", "DOR37", "DOR38", "DOR39", "CS34", "CS35", "CS9"], ["DOR68", "CS20", "ZAP29", "RE15", "RE12", "RE14", "CS17"]]}
	cluster_dic = cba.get_cluster_dic()
	begin_routing(stations_everyday)

"""Get Seconds from time."""
def get_sec(time_str):
	h, m, s = time_str.split(':')
	return int(h) * 3600 + int(m) * 60 + int(s)

"""Get travel time between two stations."""
def getTravelTime(station1, station2):
	if station1 in distance_dct and station2 in distance_dct[station1]:
		return distance_dct[station1][station2]

	if station2 in distance_dct and station1 in distance_dct[station2]:
		return distance_dct[station2][station1]
	
	if station1 not in distance_dct:
		distance_dct[station1] = {}
	
	time_station = json.load(open("time.json"))
	distance_dct[station1][station2] = time_station[station1][station2]

	return distance_dct[station1][station2]

"""Get permutation start with specific sation with minimum travel time."""
def get_permutation_start_with_station(station_list, station):
	permutations = list(itertools.permutations(station_list))
	min_time = 0
	permutation_list = []
	for stations in permutations:
		if not stations[0] == station:
			continue
		time, res = add_visit_timestamp(stations)
		if min_time == 0 or time < min_time:
			min_time = time
			permutation_list = res
	return permutation_list

def get_permutation_with_mini_time(station_list):
	permutations = list(itertools.permutations(station_list))
	min_time = 0
	permutation_list = []
	for stations in permutations:
		times, res = add_visit_timestamp(stations)
		if min_time == 0 or times < min_time:
			min_time = times
			permutation_list = res
	return permutation_list
	
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
			road_time = getTravelTime(last_station, station)
			arrival_time = departure_time + road_time

		measure_time = 150                  # inner-station time (secs)
		departure_time = arrival_time + measure_time
		last_station = station

		res.append(station)

	return departure_time, res

def begin_routing(stations_everyday):
	print('Initial path:')
	for day in stations_everyday:
		each_day = stations_everyday[day]
		dat_str = []
		for clusters in each_day:
			dat_str = dat_str + clusters
		print('day' + day + ' path: ' + str(dat_str))
				
	while(True):
		day = input("Input your current day: ")
		begin_time = input("Input your begin time: ")
		being_time = get_sec(begin_time)
		clusters = stations_everyday[day]
		del stations_everyday[day]
		last_time_repeat = 0
		current_station_index = 0
		current_cluster_index = 0
		stations = clusters[current_cluster_index]
		visit_path = []
		visit_time = []
		visit_current_time = []
		Need_to_repeat = None

		while(True):
			station_name = input("Input your current station name: ")
			current_time = input("Input your current time: ")
			
			visit_current_time.append(current_time)
			current_time = get_sec(current_time)
			
			current_time = current_time - being_time
			visit_time.append(current_time)
			
			if station_name in visit_path:
				last_time_repeat = current_time
			
			visit_path.append(station_name)
			target = stations[0]
			if station_name in stations: # If on the right station
				if Need_to_repeat != None:
					stations.remove(Need_to_repeat)
					Need_to_repeat = None
				try:
					stations.remove(station_name)
				except ValueError:
					pass
				if current_time - last_time_repeat > N:
					if len(visit_path) != 0:
						# Get travel time to visited stations
						station_travel_time = {}
						for i in range(0, len(visit_path)):
							if station_name == visit_path[i]:
								continue
							travel_time = getTravelTime(station_name, visit_path[i])

							if current_time - visit_time[i] + travel_time > N and travel_time < M:
								station_travel_time[visit_path[i]] = travel_time
						
						# Choose the station with minimum travel time
						if len(station_travel_time) > 0:
							sorted_s = sorted(station_travel_time.items(), key=operator.itemgetter(1))
							sorted_station = collections.OrderedDict(sorted_s)
							first_station = next(iter(sorted_station))
							Need_to_repeat = first_station
							# Update the new order
							new_list = []
							new_list.append(first_station)
							for station in stations:
								new_list.append(station)
							stations = get_permutation_start_with_station(new_list, first_station)
						else:
							print("Timt to visit repeat station, but no satisified stations!")
				
				elif station_name != target:
					# Update the new order
					stations = get_permutation_with_mini_time(stations)
					
				if len(stations) == 0:
					del clusters[current_cluster_index]
					current_cluster_index += 1
					if current_cluster_index >= len(clusters):
						print("You have visited all stations for today, good job!")
						break
					stations = clusters[current_cluster_index]

			travel_time = getTravelTime(station_name, stations[0])
			back_time = getTravelTime(stations[0], 'CS25')
			if current_time + travel_time + back_time > 3600 * 8:
				if Need_to_repeat != None:
					try:
						stations.remove(Need_to_repeat)
					except ValueError:
						pass
				# Cut the current cluster
				left_clusters = {}
				id = 1
				for cluster in clusters:
					left_clusters[str(id)] = {}
					left_clusters[str(id)]['visited'] = False
					left_clusters[str(id)]['stations'] = cluster
					id += 1
				for left_day in stations_everyday:
					for cluster in stations_everyday[left_day]:
						left_clusters[str(id)] = {}
						left_clusters[str(id)]['visited'] = False
						left_clusters[str(id)]['stations'] = cluster
						id += 1
			
			print("Next station is: " + stations[0])
		
		if len(stations_everyday) == 0:
			print("You have visited all stations, good job!")
			return


if __name__ == '__main__':
	main()