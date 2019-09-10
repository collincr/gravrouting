#!/usr/bin/python

import csv
import datetime

#f= open("../resources/file/inter_station_time.txt","w+")
#with open('../data/20190904_station_sequence.csv') as csv_file:
#	csv_reader = csv.reader(csv_file, delimiter=',')
#	line_count = 0
#	station = '-1'
#	prev_time = 0;
#	for row in csv_reader:
#		if line_count != 0:
#			if station != '-1' and row[4] != station:
#				date_time_obj = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
#				diff = date_time_obj - prev_time
#				f.write('<'+station+'>,<'+row[4]+'>,<'+str(diff)+'>\n')
#			station = row[4]
#			prev_time = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
#			print(prev_time)
#		line_count += 1
#	print('Processed lines.')

f = open("../resources/file/intra_measurement_time.txt","w+")
with open('../data/20190904_station_sequence.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	station = '-1'
	prev_time = 0;
	for row in csv_reader:
		if line_count != 0:
			if station != '-1' and row[4] == station:
				date_time_obj = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
				diff = date_time_obj - prev_time
				f.write('<'+station+'>,<'+str(diff)+'>\n')
			station = row[4]
			prev_time = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
			print(prev_time)
		line_count += 1
	print('Processed lines.')