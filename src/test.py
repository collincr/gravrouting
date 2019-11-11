import shortest_path as sp
from itertools import permutations 

'''
stat_dic = sp.get_station_dic()
stat_name_dic = sp.create_stat_name_id_mapping(stat_dic)
print(stat_name_dic['CS25'])
'''

nums = []
for i in range(0, 20):
    nums.append(nums)
perm = permutations(nums)
for i in list(perm): 
    print(i)
