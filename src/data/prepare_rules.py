import os
import json
import re
import jsonlines
import click


def in_rules(name):
    digit_re = re.compile('\d')
    return digit_re.search(name) or len(name) < 3

@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_file")
def prepare_rules(input_path: str, output_file: str): 
    with open(input_path) as json_file:
        dictionary = json.load(json_file)
        rules = []

        for id in dictionary.keys():
            brand = dictionary[id]
            for i in brand['names']:
                name = i['name']
                if in_rules(name): continue
                rules.append({"label": "BRAND", "pattern": [{"LOWER": name.lower()}], "id": id})
                if len(name.split(' ')) > 1:
                    rules.append({"label": "BRAND", "pattern": [{"LOWER": w.lower()} for w in name.split(' ')], "id": id })
                    
                    
            for id_model in brand['models'].keys():
                model = brand['models'][id_model]
                for i in model['names']:
                    name = i['name']
                    if in_rules(name): continue
                    rules.append({"label": "MODEL", "pattern": [{"LOWER": name.lower()}], "id": f"{id}_{id_model}"})
                    if len(name.split(' ')) > 1:
                        rules.append({"label": "MODEL", "pattern": [{"LOWER": w.lower()} for w in name.split(' ')], "id": f"{id}_{id_model}" })

        with jsonlines.open(output_file, 'w') as writer:
            writer.write_all(rules)


if __name__ == "__main__":
    prepare_rules()