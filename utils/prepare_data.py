import pandas as pd
import re
import jsonlines
from functools import cmp_to_key


def condition(word):
    return not(len(word) < 3 or word.isdecimal())

def create_prepare_file(brands,data):
    main_entities = []
    for brand in brands:
        if condition(brand['id']): main_entities.append(brand['id'])
                
        for alias in brand['alias']:
            if condition(alias): main_entities.append(alias)
                
    main_entities = [x.lower() for x in main_entities]
    main_entities = sorted(main_entities, key=cmp_to_key(lambda item1, item2: -1 if len(item2) - len(item1) < 0 else 1))

    reg = '('+'|'.join(main_entities)+')'

    str_with_space = []
    for row in data:
        string = ' '.join(re.split(reg, row, flags=re.IGNORECASE))
        string = re.sub(r'([0-9A-Z])(год|гос|белый|легк|г.в|цвет)', r'\1 \2', string, flags=re.IGNORECASE)
        string = re.sub(r'(\))([\s\w\d]*)(\))', r'\1 \2', string)
        string = re.sub(r'(\()([\d\s\w]*)(\))', r' \1\2\3 ', string)
        str_with_space.append(string)
        
    return str_with_space
