import ru_core_news_sm
import jsonlines
import os
from tqdm import tqdm
import click
import pandas as pd

from src.models.expand_model import expand_model


colors = {"BRAND": "#aa9cfc", "MODEL": "#fc9ce7", "YEAR": "#9cfcb1"}
options = {"ents": ["BRAND", "MODEL", "YEAR"], "colors": colors}


@click.command()
@click.argument("data_input_file", type=click.Path(exists=True))
@click.argument("brands_rules_file", type=click.Path(exists=True))
@click.argument("models_rules_path", type=click.Path(exists=True))
@click.argument("output_file")
def find_ner(data_input_file, brands_rules_file: str, models_rules_path: str, output_file):
    rules = list(jsonlines.open(brands_rules_file))

    for brand in os.listdir(models_rules_path):
        reader = jsonlines.open(models_rules_path + '/' + brand)
        rules = rules + list(reader)

    nlp = ru_core_news_sm.load(exclude=['tok2vec', 'morphologizer', 'parser', 'senter', 'attribute_ruler', 'lemmatizer'])

    config = {"overwrite_ents": True }
    ruler = nlp.add_pipe("entity_ruler", before="ner", config=config)

    rules.append({"label": "YEAR", "pattern": [{"LOWER": {"REGEX": "(19|20)\d{2}"}}], "id": "4-digits"})
    rules.append({"label": "YEAR", "pattern": [{"LOWER": {"REGEX": "\D(\d{2})\D"}}], "id": "2-digits"})

    ruler.add_patterns(rules)

    nlp.add_pipe("expand_model", after="ner")


    df = pd.read_excel(data_input_file)
    ents_info = []
    # html=[]
    for article in tqdm(df['vehicleproperty_description_short']):
        article = str(article)
        doc = nlp(article)
        ents_info.append(doc.user_data)
        # html.append(doc if len(doc.ents) == 0 else displacy.render(doc, style="ent", jupyter=False, options=options))

    ents_info_df = pd.DataFrame.from_records(ents_info)
    df.index.name = 'order'
    df = df.join(ents_info_df,on='order') 

    df.to_excel(output_file, index=False, encoding='utf-8')


if __name__ == "__main__":
    find_ner()
