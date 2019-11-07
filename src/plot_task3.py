#!/usr/bin/python

import csv
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import datetime
import numpy as np

def get_sec(time_str):
	h, m, s = time_str.split(':')
	return int(h) * 3600 + int(m) * 60 + int(s)

column = []
i = 0
with open('../resources/file/intra_measurement_time.txt') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	station = '-1'
	prev_time = 0
	for row in csv_reader:
		num = get_sec(row[1][1:-1])
		if num > 260 and num < 300:
			i += 1
		column.append(num)

print(column)
column = np.clip(column, 0, 260)
plt.hist(column, 
		bins=[0,100,120,130,140,150,160,170,180,190,200,220,240,260,280])
plt.savefig('../resources/img/station_visit_freq.png',
            dpi=1080)
plt.show()