import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# making data frame from csv file
df = pd.read_csv("../data/ofr20181053_table1.csv", index_col ="Station")

# creating a geometry column 
geometry = [Point(xy) for xy in zip(df['X, in feet1'], df['Y, in feet1'])]

# Coordinate reference system : WGS84
crs = {'init': 'epsg:4326'}

# Creating a Geographic data frame 
gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

# TODO conversion

gdf.plot(marker='o', color='b', markersize=0.5)
plt.show()