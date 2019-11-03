import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

data_closet_at_road_geojson = '../data/closest_at_road.geojson'
data_roads_pads_network_geojson = '../data/roads_pads_network_w_stations.geojson'
local_coordinate = '''+proj=lcc +lat_1=36 +lat_2=37.25 
                 +lat_0=35.33333333333334 +lon_0=-119 
                 +x_0=609601.2192024384 +y_0=0 
                 +datum=NAD27 +units=us-ft +no_defs'''

plt.rcParams['figure.figsize'] = (30, 24)
df_stations = gpd.read_file(data_closet_at_road_geojson)
df_stations.crs = local_coordinate
df_roads = gpd.read_file(data_roads_pads_network_geojson)
df_roads.crs = local_coordinate

ax = df_roads.plot(color='black')
ax = df_stations.plot(ax=ax, color='green')

# point annotations
for x, y, label in zip(df_stations.geometry.x, df_stations.geometry.y, df_stations['NAME']):
    annot = ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")
    annot.set_visible(True)

plt.show()