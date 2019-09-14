import csv
import pandas as pd
import json

data_stat_status_csv = '../data/20190829_stn_status.csv'
data_closet_at_road_geojson = '../data/closest_at_road.geojson'

stat_info_dic = {}

df = pd.read_csv(data_stat_status_csv, index_col='StationNumber')
stat_info_dic = df.to_dict('index')

#print(df.head())
#print(stat_info_dic)

stat_coord_dic = {}
with open(data_closet_at_road_geojson) as f:
    data_at_road = json.load(f)
for feature in data_at_road['features']:
    stat_name = feature['properties']['NAME']
    coordinates = feature['geometry']['coordinates']
    #print(stat_name, coordinates)
    stat_coord_dic[stat_name] = coordinates 

#print(stat_coord_dic)

for id_key in stat_info_dic:
    station_name = stat_info_dic.get(id_key)['StationName']
    #print(station_name)
    coordinates = stat_coord_dic.get(station_name)
    stat_info_dic.get(id_key)['coordinates'] = coordinates

#print(stat_info_dic)

stat_info_dic_json = json.dumps(stat_info_dic)
f = open("../resources/file/stat_info_dictionary.json","w")
f.write(stat_info_dic_json)
f.close()
