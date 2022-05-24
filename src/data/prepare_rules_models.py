import jsonlines
import click

from src.data.utils import create_rules


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file")
def prepare_rules_models(input_file: str, output_file: str):
    models = jsonlines.open(input_file)
    brand = input_file.split('/')[-1].split('.jsonl')[0]
    rules_model = create_rules(models, label='MODEL', prefix=brand+'_')
    with jsonlines.open(output_file, mode='w') as writer:
        writer.write_all(rules_model)
  

if __name__ == "__main__":
    prepare_rules_models()