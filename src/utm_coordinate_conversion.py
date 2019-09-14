import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def main():
    input_file = '../data/20190829_stn_status.csv'
    output_file = '../resources/file/utm_station_status.geojson'

    ref_src = '''+proj=lcc +lat_1=36 +lat_2=37.25 
                 +lat_0=35.33333333333334 +lon_0=-119 
                 +x_0=609601.2192024384 +y_0=0 
                 +datum=NAD27 +units=us-ft +no_defs'''

    ref_dst = '+proj=utm +zone=11 +datum=WGS84'

    # convert data to UTM coordinate system
    print("Data converting to UTM coordinate system...")
    gdf = data_converter('csv', input_file, 
            'Easting', 'Northing', ref_src, ref_dst)

    # save geodataframe as geojson file
    geojson_saver(gdf, output_file)

    print(gdf.head())


def data_converter(file_type, file_path, 
        x_column, y_column, ref_src, ref_dst):

    if file_type == 'geojson':

        # read file with geopandas built-in method 
        gdf = gpd.read_file(file_path)

    elif file_type == 'csv':

        # making data frame from csv file
        df = pd.read_csv(file_path)

        # creating a geometry column 
        geometry = [Point(xy) for xy in zip(df[x_column], df[y_column])]

        # original coordinate reference system
        crs = ref_src

        # creating a Geographic data frame 
        gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

    else:

        # invalid file type
        return None    

    # coordinate system conversion
    gdf = gdf.to_crs(ref_dst)

    return gdf


def geojson_saver(gdf, file_path):

    # save as geojson file
    gdf.to_file(file_path, driver='GeoJSON')


if __name__ == '__main__':
    main()
