#!/usr/bin/python

import csv
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import datetime
import numpy as np
from scipy.stats import norm


def get_sec(time_str):
	h, m, s = time_str.split(':')
	return int(h) * 3600 + int(m) * 60 + int(s)

column = []
i = 0
with open('../resources/file/intra_measurement_time.txt') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	station = '-1'
	prev_time = 0;
	for row in csv_reader:
		num = get_sec(row[1][1:-1])
		if num > 260 and num < 300:
			i += 1
		column.append(num)

print(column)
column = np.clip(column, 0, 260)

mean,std=norm.fit(column)
print(mean)
print(std)
plt.hist(column, bins=30, normed=True)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
y = norm.pdf(x, mean, std)
plt.plot(x, y)
plt.show()

#ax = sns.distplot(column,
#			bins=30,
#			kde=True,
#			hist_kws={"linewidth": 15,'alpha':1},
#			kde_kws={"color": "k", "lw": 3, "label": "KDE"})
#ax.set(xlabel='Uniform Distribution ', ylabel='Frequency')
#plt.show()
#ax = sns.distplot(column,
#			bins=30,
#			kde=True,
#			hist_kws={"linewidth": 15,'alpha':1},
#			kde_kws={"color": "k", "lw": 3, "label": "KDE"})
#ax.set(xlabel='Uniform Distribution ', ylabel='Frequency')
#plt.show()

#plt.hist(column, bins=[0,100,120,130,140,150,160,170,180,190,200,220,240,260,280])
#plt.show()