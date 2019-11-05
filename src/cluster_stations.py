import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import shortest_path as sp
import files

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

def main():
    stat_dic = sp.get_station_dic()
    X = np.array(get_stat_samples_from_dic(stat_dic))
    #print(X)
    y_pred = KMeans(n_clusters=10, random_state=100).fit_predict(X)
    #print(y_pred)
    plt.rcParams['figure.figsize'] = (15, 10)
    df_roads = gpd.read_file(files.roads_pads_network_utm_geojson)
    df_roads.plot(color='black')
    plt.scatter(X[:, 0], X[:, 1], c=y_pred)
    plt.show()
    pass

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
