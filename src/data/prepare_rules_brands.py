import jsonlines
import click

import src.data.utils as utils


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file")
def prepare_rules_brands(input_file: str, output_file: str):
    brands = list(jsonlines.open(input_file))
    rules = utils.create_rules(brands)

    with jsonlines.open(output_file, mode='w') as writer:
        writer.write_all(rules)


if __name__ == "__main__":
    prepare_rules_brands()