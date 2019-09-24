import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from data_readin_conversion import gdf_constructor, utm_coordinate_converter

def main():
    data_closet_at_road_geojson = '../data/closest_at_road.geojson'
    
    print("Preparing vertex data...")

    # read in geodataframe
    gdf_stations = gpd.read_file(data_closet_at_road_geojson)

    # setting crs is a must to convert coordinate system correctly
    gdf_stations.crs = '''+proj=lcc +lat_1=36 +lat_2=37.25 
                 +lat_0=35.33333333333334 +lon_0=-119 
                 +x_0=609601.2192024384 +y_0=0 
                 +datum=NAD27 +units=us-ft +no_defs'''

    # sample vertex list given
    vertices_x = [2349220, 2349119, 2349045, 2348964, 2348748]
    vertices_y = [285174, 285470, 285767, 286110, 286595]

    gdf_vertices = get_vertices_gdf(vertices_x, vertices_y)
    plot_vertices_line(gdf_vertices)


def get_vertices_gdf(vertices_x, vertices_y):

    # convert lists to dataframe
    df_vertices = pd.DataFrame({'Easting': vertices_x, 
            'Northing': vertices_y})

    # construct geodataframe from dataframe
    gdf_vertices = gdf_constructor(df_vertices, 
            'Easting', 'Northing')

    return gdf_vertices


def plot_vertices_line(gdf_vertices):
    ax = gdf_vertices.plot(color='green')

    # plot the whole route map for reference
    data_roads_pads_network_geojson = '../data/roads_pads_network_w_stations.geojson'
    df_roads = gpd.read_file(data_roads_pads_network_geojson)
    df_roads.plot(ax=ax, color='black')

    plt.show()
    return


if __name__ == '__main__':
    main()
