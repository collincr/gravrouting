import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from data_readin_conversion import gdf_constructor, utm_coordinate_converter

def main():
    local_gravity_change_csv = '../data/ofr20181053_table1.csv'

    print("Data converting to UTM coordinate system...")

    # read in dataframe
    df_gravity = pd.read_csv(local_gravity_change_csv)

    # construct geodataframe from dataframe
    gdf_gravity = gdf_constructor(df_gravity, 
            'X, in feet1', 'Y, in feet1')

    # convert coordinate system to utm
    gdf_gravity = utm_coordinate_converter(gdf_gravity)

    print(gdf_gravity.head())

    print("\nData visualizing...")

    # visualization
    gravity_change_visualizer(gdf_gravity, False)


def gravity_change_visualizer(gdf, if_annot):

    # overall settings
    fig, ax = plt.subplots(1, figsize=(8, 8))
    ax = gdf.plot(column='Change in gravity (∆G), in milliGals',
            cmap='rainbow', ax=ax, legend=True)

    # label settings
    plt.title('Station Gravity Change', fontsize=14)
    plt.xlabel('Easting [meters]', fontsize=13)
    plt.ylabel('Northing [meters]', fontsize=13)

    # axis settings
    ax.set_autoscaley_on(False)

    x_min = gdf.geometry.x.min()
    x_max = gdf.geometry.x.max()
    x_range = x_max - x_min

    y_min = gdf.geometry.y.min()
    y_max = gdf.geometry.y.max()
    y_range = y_max - y_min

    ax.set_xlim([x_min - x_range * 0.1, x_max + x_range * 0.1])
    ax.set_ylim([y_min - y_range * 0.1, y_max + y_range * 0.1])
    ax.legend(['gravity change [milligals]'])

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
