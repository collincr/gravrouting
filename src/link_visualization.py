import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from shapely.geometry import LineString
from graph_util import create_adj_vertex_dic

def main():
    data_closet_at_road_geojson = '../data/closest_at_road.geojson'
    data_roads_pads_network_geojson = '../data/roads_pads_network_w_stations.geojson'

    crs = '''+proj=lcc +lat_1=36 +lat_2=37.25 
             +lat_0=35.33333333333334 +lon_0=-119 
             +x_0=609601.2192024384 +y_0=0 
             +datum=NAD27 +units=us-ft +no_defs'''

    print("Preparing vertex data...")

    # sample vertex list given
    vertices_x = [2330062, 2327545, 2327522, 2324752, 2324501, 2324309, 2323926, 2323503, 2323203, 2323077, 2322839, 2322614, 2322306, 2322012, 2321773, 2321577, 2321409, 2321213, 2320007, 2319320, 2318605, 2318226, 2317988, 2317638, 2317329, 2315451, 2315156, 2314988, 2314848, 2314666, 2314483, 2314301, 2313965, 2313516, 2312451, 2311708, 2311610, 2311399, 2311049]
    vertices_y = [241357, 242506, 242516, 243816, 243926, 243896, 243977, 244178, 243977, 243921, 243893, 243822, 243738, 243612, 243472, 243472, 243430, 243346, 242701, 242463, 242210, 241972, 241635, 241117, 240794, 239182, 238902, 238691, 238481, 238285, 238131, 237948, 237626, 237290, 236406, 235734, 235635, 235537, 235355]

    gdf_lines = get_lines_gdf(vertices_x, vertices_y, crs, 
            data_roads_pads_network_geojson)
    plot_lines(gdf_lines, crs, data_roads_pads_network_geojson, 
            data_closet_at_road_geojson)


def get_lines_gdf(vertices_x, vertices_y, crs,
            data_roads_pads_network_geojson):
    coords = []

    # create vertex adjancency dictionary
    vertex_dictionary = create_adj_vertex_dic(
            data_roads_pads_network_geojson)

    # construct connected lines
    for i in range(len(vertices_x)):
        for j in range(i + 1, len(vertices_x)):
            vertex_id = vertex_dictionary.get(str(vertices_x[i]) 
                    + '#' + str(vertices_y[i]))['id']
            vertex_adjs = vertex_dictionary.get(str(vertices_x[j]) 
                    + '#' + str(vertices_y[j]))['adj']
            if vertex_id in vertex_adjs:
                conn = (vertices_x[i], vertices_y[i]), (vertices_x[j], vertices_y[j])
                line_string = LineString(conn)
                coords.append(line_string)
            
    # creating lines' geographic dataframe 
    gdf_lines = gpd.GeoDataFrame(crs=crs, geometry=coords)

    return gdf_lines


def plot_lines(gdf_lines, crs, data_roads_pads_network_geojson, 
            data_closet_at_road_geojson):
    plt.rcParams['figure.figsize'] = (30, 24)

    # plot the whole route map and stations for reference
    gdf_roads = gpd.read_file(data_roads_pads_network_geojson)
    gdf_stations = gpd.read_file(data_closet_at_road_geojson)
    gdf_roads.crs = crs    # setting up crs is a must
    gdf_stations.crs = crs

    # to avoid a feature covered by another, the sequence of plot matters
    ax = gdf_roads.plot(color='black')
    ax = gdf_lines.plot(ax=ax, color='green', linewidth=5)
    gdf_stations.plot(ax=ax, color='red', markersize=50)

    plt.title('Road links')
    plt.xlabel('Easting (ft)', fontsize=13)
    plt.ylabel('Northing (ft)', fontsize=13)

    plt.show()
    return


if __name__ == '__main__':
    main()
