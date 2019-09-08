import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

def main():
    file_path = "../data/ofr20181053_table1.csv";

    ref_src = '''+proj=lcc +lat_1=36 +lat_2=37.25 
                 +lat_0=35.33333333333334 +lon_0=-119 
                 +x_0=609601.2192024384 +y_0=0 
                 +datum=NAD27 +units=us-ft +no_defs'''

    ref_dst = '+proj=utm +zone=11 +datum=WGS84'

    # convert data to UTM coordinate system
    gdf = data_converter(file_path, ref_src, ref_dst)
    print(gdf.head())

    # visualization
    data_visualizer(gdf)


def data_converter(file_path, ref_src, ref_dst):

    # making data frame from csv file
    df = pd.read_csv(file_path, index_col ="Station")

    # creating a geometry column 
    geometry = [Point(xy) for xy in zip(df['X, in feet1'], df['Y, in feet1'])]

    # original coordinate reference system
    crs = ref_src

    # creating a Geographic data frame 
    gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

    # coordinate system conversion
    gdf = gdf.to_crs(ref_dst)

    return gdf


def data_visualizer(gdf):
    gdf.plot(marker='o', color='b', markersize=0.5)
    plt.show()


if __name__ == '__main__':
    main()