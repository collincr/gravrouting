import shortest_path as sp
import cluster_by_agglomerative as cba

def main():
	station_sequence = ["B-15", "DOR64", "DOR65", "DOR66", "CS1", "B-14", "DOR68"]
	cluster_dic = cba.get_cluster_dic()
	print(cluster_dic)

def begin_routing():
	while(True):
		station_name = input("Input your current station name: ")
		current_time = input("Input your current time: ")
		
		if station_name == 'y':
			print('1')
		else:
			break

if __name__ == '__main__':
	main()