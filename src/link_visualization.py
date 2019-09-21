import geopandas as gpd
from utm_coordinate_conversion import gdf_constructor, utm_coordinate_converter

def main():
    data_closet_at_road_geojson = '../data/closest_at_road.geojson'
    
    print("Data converting to UTM coordinate system...")

    # read in geodataframe
    gdf_stations = gpd.read_file(data_closet_at_road_geojson)
    gdf_stations.crs = '''+proj=lcc +lat_1=36 +lat_2=37.25 
                 +lat_0=35.33333333333334 +lon_0=-119 
                 +x_0=609601.2192024384 +y_0=0 
                 +datum=NAD27 +units=us-ft +no_defs'''

    # convert coordinate system to utm
    gdf_stations = utm_coordinate_converter(gdf_stations)
    

if __name__ == '__main__':
    main()