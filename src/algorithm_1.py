import datetime as dt
import collections
import operator
from shortest_path import internal_get_spt_from_stat_name

def main():
	station_list = {'CS25', 'CS26', 'COSO2', 'CS44', 'CS43'}
	#permutation_list = get_permutation_with_mini_time(station_list)
	permutation_list = ['CS44', 'COSO2', 'CS43', 'CS25', 'CS26']
	simulate_visit_station(permutation_list)

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
	speed = 10
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

		visit_path.append(current_station)
		visit_time.append(current_time)
		
		# Simulate the test time
		current_time = current_time + test_time

		if current_time - last_time_repeat > N:
			if len(visit_path) == 0:
				print("Error!!!!!!!!!!!!!!!!!!!!!!!!!")
			else:
				station_travel_time = {}
				for i in range(0, len(visit_path)):
					_, distance = internal_get_spt_from_stat_name(current_station, visit_path[i])
					travel_time = distance // speed
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
			_, distance = internal_get_spt_from_stat_name(current_station, next_station)
			travel_time = distance // speed
			current_time += travel_time
			current_station = next_station
	
	print("final path:")
	print(visit_path)
	print(visit_time)
		


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
			_, distance = internal_get_spt_from_stat_name(last_station, station)
			road_time = distance // speed   # intra-station time (secs)
			arrival_time = departure_time + road_time

		measure_time = 150                  # inner-station time (secs)
		departure_time = arrival_time + measure_time
		last_station = station

		res.append(station)

	return departure_time, res


if __name__ == '__main__':
	main()