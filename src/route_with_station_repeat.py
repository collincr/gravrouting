import threading
from shortest_path import internal_get_spt_from_stat_name

# N minites, 90 mins by default
REPEAT_INTERVAL = 5400

# M minutes, 15 mins by default
MIN_REPEAT_INTERVAL = 900

# Global boolean flag
already_repeat = True


def main():
    repeat_station()


def repeat_station():

    # All previously visited stations
    visited_stations = list()

    # Time elapsed since last visit of visited_stations at accoding index
    time_elapsed = list() 

    repeat(True)


''' Timer for flag on whether already repeated.
''' 
def repeat(first):
    if not first:
        global already_repeat
        already_repeat = False
        print("Repeat interval elapsed.")
    threading.Timer(REPEAT_INTERVAL, repeat, (False,)).start()
    

def find_station_to_repeat(curr_station, visited_stations, time_elapsed):
    nearest_visited = None
    min_dist = float('inf')
    for i in range(len(visited_stations)):
        if time_elapsed[i] < MIN_REPEAT_INTERVAL:
            continue
        _, dist = internal_get_spt_from_stat_name(curr_station, visited_stations[i])
        if dist < min_dist:
            min_dist = dist
            nearest_visited = visited_stations[i]
    return nearest_visited, min_dist


if __name__ == '__main__':
    main()
