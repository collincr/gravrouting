import numpy as np
import matplotlib.pyplot as plt
import shortest_path as sp

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

def main():
    stat_dic = sp.get_station_dic()
    X = np.array(get_stat_samples_from_dic(stat_dic))
    #print(X)
    y_pred = KMeans(n_clusters=19, random_state=100).fit_predict(X)
    plt.figure(figsize=(12, 12))
    plt.subplot(221)
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
