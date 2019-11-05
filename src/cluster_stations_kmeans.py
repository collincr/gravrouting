import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import shortest_path as sp
import files

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from scipy.spatial.distance import cdist

def main():
    #determine_k_by_elbow()
    plot_stations_cluster(17)
    pass

def determine_k_by_elbow():
    stat_dic = sp.get_station_dic()
    X = np.array(get_stat_samples_from_dic(stat_dic))
    distortions = []
    K = range(1,20)
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(X)
        kmeanModel.fit(X)
        distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.xlim([0, 20])
    plt.savefig('../resources/img/elbow_method.png', dpi=1000)
    plt.show()

def plot_stations_cluster(k):
    stat_dic = sp.get_station_dic()
    X = np.array(get_stat_samples_from_dic(stat_dic))
    #print(X)
    kmeans = KMeans(n_clusters=k, random_state=100)
    y_pred = kmeans.fit_predict(X)
    #print(y_pred)
    plt.rcParams['figure.figsize'] = (15, 10)
    df_roads = gpd.read_file(files.roads_pads_network_utm_geojson)
    df_roads.plot(color='black')
    plt.scatter(X[:, 0], X[:, 1], c=y_pred)
    
    if False:
        for stat_id in stat_dic:
            label = stat_dic[stat_id]['name']
            e = stat_dic[stat_id]['road_coordinates'][0]
            n = stat_dic[stat_id]['road_coordinates'][1]
            plt.annotate(label, xy=(e, n), xytext=(e+10, n+10))
    # Plot centroids
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,color='r', zorder=10)

    plt.title('Stations with ' +  str(k) + ' clusters')
    plt.xlabel('Easting [m]', fontsize=13)
    plt.ylabel('Northing [m]', fontsize=13)

    filename = '../resources/img/' + str(k) + '_clusters_stations.png'
    plt.savefig(filename, dpi=1000)
    plt.show()

def get_stat_samples_from_dic(stat_dic):
    samples = []
    for stat_id in stat_dic:
        road_coordinate = stat_dic[stat_id]['road_coordinates']
        sample = [road_coordinate[0], road_coordinate[1]]
        #print(sample)
        samples.append(sample)
    #print(samples)
    return samples

if __name__ == '__main__':
    main()
