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

    # calculate distance
    print("Each pair of distances calculating...")
    dist = pair_distance(gdf)
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