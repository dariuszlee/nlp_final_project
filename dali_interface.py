import DALI as dali_code

dali_data_path = '/home/dzly/masters/y2s1/natural_language/final/src/dali/'
dali_data = dali_code.get_the_DALI_dataset(dali_data_path, skip=[], keep=[])

dali_info = dali_code.get_info(dali_data_path + 'info/DALI_DATA_INFO.gz')
print(dali_info[0])

artists = set()
for data_row in dali_info[1:]:
    artists.add(dali_data[data_row[0]].info['artist'])

__import__('ipdb').set_trace()
print("Asdf")

