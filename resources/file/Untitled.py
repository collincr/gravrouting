from collections import OrderedDict
import collections
import json
import time
import linecache


def ff():
	return 

f = open("inter_station_time2.txt", "r")
for x in f:
	temp = x.split(" ")
	route = temp[0]
	time = float(temp[1]) * 60
	type = temp[-1]
	name = route.split("->")
	a = ff()
	if a == None:
		print("@@")
	print(a)
