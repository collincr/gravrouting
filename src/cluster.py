# import KMeans
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import geopandas as gpd

# import hierarchical clustering libraries
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering

from shortest_path import get_station_dic
import shortest_path as sp
from shortest_path import internal_get_spt_from_stat_name
import pickle

cluster_num = 9
recluster_num = 3
cluster_size_limit = 13

label = 0

def computeDisMetrix():
	staion_dic = get_station_dic()
	id_name = {}
	id = 0
	for station in staion_dic:
		id_name[staion_dic[station]['name']] = id
		id += 1
	
	dis_metrix = [([0] * len(id_name)) for i in range(len(id_name))]
	
	road_network_dic, station_info_dic = sp.preprocess()
	stations_shortest_path_dic = sp.get_all_stations_spt_dic_from_file()
	
	for station in id_name:
		for station1 in id_name:
			if station is not station1:
				distance = 0
				print(station+"#"+station1)
				distance, path = sp.get_shortest_path(station, station1, station_info_dic,
							stations_shortest_path_dic)
				if distance == None:
					_, distance = internal_get_spt_from_stat_name(station, station1)
	
				dis_metrix[id_name[station]][id_name[station1]] = distance
				dis_metrix[id_name[station1]][id_name[station]] = distance
	
	return dis_metrix


def reCluster(dirmap):
	# Re-cluster
	global label
	dis_metrix = [([0] * len(dirmap)) for i in range(len(dirmap))]
	for station in range(0,len(dirmap)):
		for station1 in range(0,len(dirmap)):
			if station != station1:
				dis_metrix[station][station1] = itemlist[dirmap[station]][dirmap[station1]]
				dis_metrix[station1][station] = itemlist[dirmap[station]][dirmap[station1]]
	
	recluster_num = int(len(dirmap) / 7)
	hc2 = AgglomerativeClustering(n_clusters=recluster_num, affinity = 'precomputed', linkage = 'average')
	dis_metrix = np.array(dis_metrix)
	y_hc2 = hc2.fit_predict(dis_metrix)
	
	number = 1
	for sub2 in range(0,recluster_num):
		num = 0
		if np.count_nonzero(y_hc2 == sub2) > cluster_size_limit:
			dirmap2 = {}
			index = 0
			for i in range(0, len(y_hc2)):
				if sub2 == y_hc2[i]:
					dirmap2[index] = dirmap[i]
					index += 1
			reCluster(dirmap2)
		else:
			for i in range(0, len(y_hc2)):
				if sub2 == y_hc2[i]:
					x = loc[dirmap[i], 0]
					y = loc[dirmap[i], 1]
					plt.annotate(str(label), (x+50, y+50))
					num += 1
			print(str(label)+": "+str(num))
			label += 1
		
		
		
#dis_metrix = computeDisMetrix()

itemlist = None
with open ('outfile', 'rb') as fp:
	itemlist = pickle.load(fp)
	# print(itemlist)
itemlist = np.array(itemlist)

# create scatter plot
staion_dic = get_station_dic()

loc = []
xmin = 5000000
xmax = 0
ymin = 50000000
ymax = 0
for station in staion_dic:
	loc.append(staion_dic[station]['coordinates'])
	if staion_dic[station]['coordinates'][0] < xmin:
		xmin = staion_dic[station]['coordinates'][0]
	
	if staion_dic[station]['coordinates'][0] > xmax:
		xmax = staion_dic[station]['coordinates'][0]
	
	if staion_dic[station]['coordinates'][1] < ymin:
		ymin = staion_dic[station]['coordinates'][1]
	
	if staion_dic[station]['coordinates'][1] > ymax:
		ymax = staion_dic[station]['coordinates'][1]

loc = np.array(loc)

#plt.scatter(loc[:,0], loc[:,1], c='red', cmap='viridis', s = 20)
#plt.xlim(xmin - 1000,xmax + 1000)
#plt.ylim(ymin - 1000,ymax + 1000)# create kmeans object
#
#plt.show()

#kmeans = KMeans(n_clusters=4)
## fit kmeans object to data
#kmeans.fit(points)
## print location of clusters learned by kmeans object
#print(kmeans.cluster_centers_)
## save new clusters for chart
#y_km = kmeans.fit_predict(points)
#
#plt.scatter(points[y_km ==0,0], points[y_km == 0,1], s=20, c='red')
#plt.scatter(points[y_km ==1,0], points[y_km == 1,1], s=100, c='black')
#plt.scatter(points[y_km ==2,0], points[y_km == 2,1], s=100, c='blue')
#plt.scatter(points[y_km ==3,0], points[y_km == 3,1], s=100, c='cyan')

# create dendrogram
# dendrogram = sch.dendrogram(sch.linkage(points, method='ward'))
# create clusters

#hc = AgglomerativeClustering(n_clusters=4, affinity = 'euclidean', linkage = 'ward')
#y_hc = hc.fit_predict(points)

hc = AgglomerativeClustering(n_clusters=cluster_num, affinity = 'precomputed', linkage = 'average')
y_hc = hc.fit_predict(itemlist)

colors = cm.rainbow(np.linspace(0, 1, cluster_num))

i = 0
for c in colors:
	plt.scatter(loc[y_hc ==i,0], loc[y_hc == i,1], s=20, color=c)
	i+=1

for sub in range(0,cluster_num):
	x = loc[y_hc ==sub,0]
	y = loc[y_hc ==sub,1]
	num = 0
	if len(x) > cluster_size_limit:
		dirmap = {}
		index = 0
		for i in range(0, len(y_hc)):
			if y_hc[i] == sub:
				dirmap[index] = i
				index += 1
		reCluster(dirmap)
	else:	
		for j in range(0,len(x)):
			plt.annotate(label, (x[j]+50, y[j]+50))
			num += 1
		print(str(label)+": "+str(num))
		label += 1


plt.show()