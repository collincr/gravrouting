from utm_coordinate_conversion import gdf_constructor, utm_coordinate_converter

def main():
    local_station_status_csv = '../data/20190829_stn_status.csv'
    
    print("Data converting to UTM coordinate system...")
    
    # read in dataframe
    df_stations = pd.read_csv(local_station_status_csv)

    # construct geodataframe from dataframe
    gdf_stations = gdf_constructor(df_stations, 'Easting', 'Northing')

    # convert coordinate system to utm
    gdf_stations = utm_coordinate_converter(gdf_stations)

    print("Each pair of distances calculating...")

    # calculate distance
    dist = pair_distance(gdf_stations)
    
    print(dist)


def pair_distance(gdf):
    distances = {}
    for i in range(gdf.geometry.size - 1):
        for j in range(i + 1, gdf.geometry.size):
            
            # station names
            point_a = gdf.loc[i]['Station']
            point_b = gdf.loc[j]['Station']
            
            # euclidean distance
            dist = gdf.geometry.iloc[i].distance(gdf.geometry.iloc[j])
            
            # symmetric so add both
            distances[point_a + " " + point_b] = dist
            distances[point_b + " " + point_a] = dist

    return distances


if __name__ == '__main__':
    main()