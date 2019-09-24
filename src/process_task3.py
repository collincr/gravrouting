#!/usr/bin/python

import csv
import datetime
from collections import OrderedDict

f= open("../resources/file/inter_station_time2.txt","w+")
key_dic = OrderedDict()
with open('../data/20190904_station_sequence.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	station = '-1'
	prev_time = 0;
	for row in csv_reader:
		if line_count != 0:
			if station != '-1' and row[5] != station:
				date_time_obj = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
				diff = date_time_obj - prev_time
				diff = round(diff.total_seconds()/60,2)
				stationPair = station + '->' + row[5]
				stationPair2 = row[5] + '->' + station
				if stationPair in key_dic:
					key_dic[stationPair].append(diff)
				elif stationPair2 in key_dic:
					key_dic[stationPair2].append(diff)
				else:
					temp = []
					temp.append(diff)
					key_dic[stationPair] = list(temp)
				#f.write('<'+station+'>,<'+row[5]+'>,<'+str(diff)+'>\n')
			station = row[5]
			prev_time = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
		line_count += 1
	print('Processed lines.')

for key in key_dic:
	seperator = ', '
	avg = 0
	res = []
	for time in key_dic[key]:
		res.append(str(time))
	avg = round(sum(key_dic[key]) / len(key_dic[key]), 2)
	strs = seperator.join(res)
	if len(key_dic[key]) == 1:
		f.write(key+': \t'+strs+'\n')
	else:
		f.write(key+': \t'+strs+'    Average: ' + str(avg)+'\n')
#f = open("../resources/file/intra_measurement_time.txt","w+")
#with open('../data/20190904_station_sequence.csv') as csv_file:
#	csv_reader = csv.reader(csv_file, delimiter=',')
#	line_count = 0
#	station = '-1'
#	prev_time = 0;
#	for row in csv_reader:
#		if line_count != 0:
#			if station != '-1' and row[4] == station:
#				date_time_obj = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
#				diff = date_time_obj - prev_time
#				f.write('<'+station+'>,<'+str(diff)+'>\n')
#			station = row[4]
#			prev_time = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
#			print(prev_time)
#		line_count += 1
#	print('Processed lines.')