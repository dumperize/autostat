import os
import json


path = 'data/raw/brand_with_models/'
list_files = os.listdir(path)
dictionary = {}
for file in list_files:
    with open(path + file, 'r') as outfile:
        data = json.load(outfile)
        name = data['id']
        dictionary[name] = data
