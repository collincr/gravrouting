#!/usr/bin/python

import csv
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import datetime
import numpy as np
from scipy.stats import norm
import scipy


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

#print(column)
data = np.clip(column, 0, 260)
plt.hist(data, bins=30, normed=True)
x = np.linspace(100, 260, 100)
#print(x)
dist_names = ['gamma', 'beta', 'rayleigh', 'norm', 'pareto']
for dist_name in dist_names:
	dist = getattr(scipy.stats, dist_name)
	param = dist.fit(data)
	print(dist_name)
	print(param[-1])
	print(param[-2])
	print("\n")
	pdf_fitted = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1])
	plt.plot(x, pdf_fitted, label=dist_name)
plt.legend(loc='upper right')
plt.show()