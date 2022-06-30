import json
import re
import jsonlines
import click


digit_re = re.compile('\d')
skob_re = re.compile('[\(\)]')
def condition(name):
    return not digit_re.search(name) and len(name) > 3 and not skob_re.search(name)

@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("file_important_names_add", type=click.Path(exists=True))
@click.argument("file_important_names_remove", type=click.Path(exists=True))
@click.argument("output_file")
def prepare_important_names(input_file: str, file_important_names_add: str, file_important_names_remove:str, output_file: str): 
    important_names = list(jsonlines.open(file_important_names_add))
    important_names_remove = list(jsonlines.open(file_important_names_remove))

    with open(input_file) as json_file:
        dictionary = json.load(json_file)


        for x in dictionary.keys():
            brand = dictionary[x]
            names = [item['name'] for item in brand['names'] if condition(item['name'])]
            important_names.extend(names)

            for model in brand['models'].values():
                names = [item['name'] for item in model['names'] if condition(item['name'])]
                important_names.extend(names)

        important_names = sorted(list(set(important_names)), key=len, reverse=True)
        important_names = list(map(lambda x: x.lower(), important_names))   
        important_names = list(filter(lambda x: x not in important_names_remove, important_names))


        with jsonlines.open(output_file, 'w') as writer:
            writer.write_all(important_names)


if __name__ == "__main__":
    prepare_important_names()