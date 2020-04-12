import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def main():
    local_station_status_csv = '../data/20190829_stn_status.csv'
    utm_station_status_geojson = '../resources/file/utm_station_status.geojson'    
    app_station_status_geojson = '../resources/file/app_station_status.geojson'

    print("Data converting to UTM coordinate system...")
    
    # read in dataframe
    df_stations = pd.read_csv(local_station_status_csv)

    # construct geodataframe from dataframe
    gdf_stations = gdf_constructor(df_stations, 'Easting', 'Northing')

    # convert coordinate system to utm
    #gdf_stations = utm_coordinate_converter(gdf_stations)
    gdf_stations = app_coordinate_converter(gdf_stations)
    # save geodataframe as geojson file
    geojson_saver(gdf_stations, app_station_status_geojson)

    print(gdf_stations.head())


def gdf_constructor(df, x_column, y_column):

    # original coordinate reference system
    local_coordinate = '''+proj=lcc +lat_1=36 +lat_2=37.25 
                 +lat_0=35.33333333333334 +lon_0=-119 
                 +x_0=609601.2192024384 +y_0=0 
                 +datum=NAD27 +units=us-ft +no_defs'''

    # creating a geometry column 
    geometry = [Point(xy) for xy in zip(df[x_column], df[y_column])]

    # creating a Geographic data frame 
    gdf = gpd.GeoDataFrame(df, crs=local_coordinate, geometry=geometry)  

    return gdf


def utm_coordinate_converter(gdf):

    # target coordinate reference system
    utm_coordinate = '+proj=utm +zone=11 +datum=WGS84'

    # coordinate system conversion
    gdf = gdf.to_crs(utm_coordinate)

    return gdf

def app_coordinate_converter(gdf):

    # target coordinate reference system
    app_coordinate = '+proj=latlong +datum=WGS84'

    # coordinate system conversion
    gdf = gdf.to_crs(app_coordinate)

    return gdf

def convert_to_UTM_with_geojson(geojson):
    gdf_roads = gpd.read_file(geojson)
    #print(gdf_roads.head())
    #print('\n')
    local_coordinate = '''+proj=lcc +lat_1=36 +lat_2=37.25
                 +lat_0=35.33333333333334 +lon_0=-119
                 +x_0=609601.2192024384 +y_0=0
                 +datum=NAD27 +units=us-ft +no_defs'''
    gdf_roads.crs  = local_coordinate
    gdf_roads_UTM = utm_coordinate_converter(gdf_roads)
    #print(gdf_roads_UTM.head())
    return gdf_roads_UTM

def geojson_saver(gdf, file_path):

    # save as geojson file
    gdf.to_file(file_path, driver='GeoJSON')


if __name__ == '__main__':
    main()
