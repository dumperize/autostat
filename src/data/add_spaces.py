import jsonlines
import click
import re
import os
from functools import cmp_to_key
import pandas as pd


def condition(word):
    return not(len(word) < 3 or word.isdecimal())

def create_prepare_file(brands, data):
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
        string = re.sub(r'([0-9A-Z])(год|гос|белый|легк|г.в|цвет|тип)', r'\1 \2', string, flags=re.IGNORECASE)
        string = re.sub(r'(максима) (льная)', r'\1\2', string, flags=re.IGNORECASE)
        string = re.sub(r'([0-9])(VIN)', r'\1 \2', string, flags=re.IGNORECASE)
        string = re.sub(r'(\))([\s\w\d]*)(\))', r'\1 \2', string)
        string = re.sub(r'(\()([\d\s\w]*)(\))', r' \1\2\3 ', string)
        str_with_space.append(string)
        
    return str_with_space

@click.command()
@click.argument("data_input_file", type=click.Path(exists=True))
@click.argument("brands_input_file", type=click.Path(exists=True))
@click.argument("path_to_models", type=click.Path(exists=True))
@click.argument("output_file")
def add_spaces(data_input_file: str, brands_input_file:str, path_to_models:str, output_file: str):
    BRANDS = os.listdir(path_to_models)
    list_rules = list(jsonlines.open(brands_input_file))
    for x in BRANDS:
        reader = jsonlines.open(path_to_models + '/' + x)
        list_rules = list_rules + list(reader)  
    
    data = pd.read_csv(data_input_file, delimiter='|')
    str_with_space = create_prepare_file(data=data['vehicleproperty_description_short'].values, brands=list_rules)

    data['vehicleproperty_description_short'] = str_with_space

    data.to_excel(output_file, index=False)


if __name__ == "__main__":
    add_spaces()