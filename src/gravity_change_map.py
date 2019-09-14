import geopandas as gpd
import matplotlib.pyplot as plt
from utm_coordinate_conversion import data_converter

def main():
    input_path = '../data/ofr20181053_table1.csv'

    ref_src = '''+proj=lcc +lat_1=36 +lat_2=37.25 
                 +lat_0=35.33333333333334 +lon_0=-119 
                 +x_0=609601.2192024384 +y_0=0 
                 +datum=NAD27 +units=us-ft +no_defs'''

    ref_dst = '+proj=utm +zone=11 +datum=WGS84'

    # convert data to UTM coordinate system
    print("Data converting to UTM coordinate system...")
    gdf = data_converter('csv', input_path, 'X, in feet1', 
            'Y, in feet1', ref_src, ref_dst)
    print(gdf.head())

    # visualization
    print("\nData visualizing...")
    gravity_change_visualizer(gdf, False)


def gravity_change_visualizer(gdf, if_annot):

    # overall settings
    fig, ax = plt.subplots(1, figsize=(8, 8))
    ax = gdf.plot(column='Change in gravity (∆G), in milliGals',
            cmap='rainbow', ax=ax, legend=True)

    # label settings
    plt.xlabel('Easting', fontsize=13)
    plt.ylabel('Northing', fontsize=13)

    # axis settings
    ax.set_title('Station Gravity Change', fontsize=14)
    ax.set_autoscaley_on(False)

    x_min = gdf.geometry.x.min()
    x_max = gdf.geometry.x.max()
    x_range = x_max - x_min

    y_min = gdf.geometry.y.min()
    y_max = gdf.geometry.y.max()
    y_range = y_max - y_min

    ax.set_xlim([x_min - x_range * 0.1, x_max + x_range * 0.1])
    ax.set_ylim([y_min - y_range * 0.1, y_max + y_range * 0.1])

    # y:x default is 1.0
    # ax.set_aspect(0.5)

    # point annotations
    for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['Station']):
        annot = ax.annotate(label, xy=(x, y), xytext=(3, 3), 
                textcoords="offset points")
        annot.set_visible(if_annot)
        
    # save figure before showing
    plt.savefig('../resources/img/station_gravity_change.png',
            dpi=1080)
    plt.show()


if __name__ == '__main__':
    main()
