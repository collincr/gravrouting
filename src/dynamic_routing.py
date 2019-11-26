import shortest_path as sp
import cluster_by_agglomerative as cba
from cluster_routing import get_next_day_station_seq
import json
import operator
import collections
import itertools

N = 1800
M = 900
distance_dct = {}

def main():
	station_sequence = ["B-15", "DOR64", "DOR65", "DOR66", "CS1", "B-14", "DOR68"]
	stations_everyday = {1: [['CS25', 'CS21', 'RE1', 'CER15', 'RE5', 'RE38', 'ZAP15', 'SLME', 'RE7', 'RE6'], ['CSE1', 'RE4', 'CER1', 'DOR72', 'RE36'], ['CS35', 'CS9', 'CS8', 'RE36', 'DOR37', 'CS34', 'DOR38', 'DOR39'], ['CS3', 'CRJ', 'RE36', 'CW1B', 'CS7']], 2: [['CS25', 'RE3', 'RE35', 'RE2', 'CS31', 'RE39', 'COSO3', 'RE40'], ['J217', 'CS28', 'CS23', 'CS22', 'COSO3', 'CS24', 'CS66', 'CS26', 'COSO2'], ['CS43', 'COSO1', 'CS44'], ['RE13']], 3: [['CS25', 'RE13', 'RE11', 'RE34', 'RE31', 'RE32', 'CS19', 'CSE5', 'RE24', 'CS18', 'RE25'], ['CSE3', 'RE30', 'RE29', 'CS10', 'RE26', 'CS70', 'RE27A', 'RE28', 'CSE4'], ['CS13', 'CS12', 'CS11', 'CS10', 'RE33']], 4: [['CS25', 'RE9', 'RE37', 'CSE2', 'RE8', 'RE10'], ['B-14', 'DOR68', 'CS20'], ['RE14', 'RE12', 'RE18', 'CS17', 'RE19', 'CS16', 'RE22A', 'RE20', 'RE21'], ['ZAP29', 'RE15', 'RE16', 'RE17', 'ZAP28'], ['ZAP2', 'CS67'], ['CGB']], 5: [['CS25', 'CS29', 'CS52', 'J4', 'CS41', 'CS30'], ['CGB', 'CS1', 'DOR66', 'DOR65', 'DOR64', 'B-15'], ['CS37', 'CS36', 'CS38']], 6: [['CS25', 'RE33', 'CS36'], ['CS64'], ['CS63'], ['CS65', 'CS5', 'CS4', 'CS6', 'CS7'], ['J214']], 7: [['CS25', 'JOSRIDGE', 'CS15', 'CS14', 'VOLPK']]}
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
	road_network_dic, station_info_dic = sp.preprocess()
	name_to_id = {}
	for id in station_info_dic:
		name_to_id[station_info_dic[id]['name']] = id
	print('Initial path:')
	for day in stations_everyday:
		each_day = stations_everyday[day]
		dat_str = []
		for clusters in each_day:
			dat_str = dat_str + clusters
		print('day' + str(day) + ' path: ' + str(dat_str))
				
	while(True):
		day = input("Input your current day: ")
		day = int(day)
		clusters = stations_everyday[day]
		dat_str = []
		for cluster in clusters:
			dat_str = dat_str + cluster
		print('Today\'s path: ' + str(dat_str))
		
		begin_time = input("Input your begin time: ")
		being_time = get_sec(begin_time)
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
							new_list = list(set(new_list)) 
							stations = get_permutation_start_with_station(new_list, first_station)
						else:
							print("Timt to visit repeat station, but no satisified stations!")
				
				elif station_name != target:
					# Update the new order
					stations = list(set(stations)) 
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
					left_clusters[str(id)]['stations'] = []
					for stat in cluster:
						left_clusters[str(id)]['stations'].append(name_to_id[stat])
					left_clusters[str(id)]['start'] = name_to_id[cluster[0]]
					id += 1
				for left_day in stations_everyday:
					for cluster in stations_everyday[left_day]:
						left_clusters[str(id)] = {}
						left_clusters[str(id)]['visited'] = False
						left_clusters[str(id)]['stations'] = []
						for stat in cluster:
							left_clusters[str(id)]['stations'].append(name_to_id[stat])
						left_clusters[str(id)]['start'] = name_to_id[cluster[0]]
						id += 1
				print(left_clusters)
				new_stations_everyday = get_next_day_station_seq(left_clusters)
				new_day = day + 1
				stations_everyday = {}
				for days in new_stations_everyday:
					stations_everyday[new_day] = []
					for clu in new_stations_everyday[days]:
						temp = []
						for sta in clu:
							if sta not in temp:
								temp.append(sta)
						stations_everyday[new_day].append(temp)
					new_day += 1
				temp = {}
				print(stations_everyday)
				print("You have reached 8 hours limit, now you can go back to CS25")
				break
			print("Next station is: " + stations[0])
		
		if len(stations_everyday) == 0:
			print("You have visited all stations, good job!")
			return


if __name__ == '__main__':
	main()