from tqdm import tqdm
import click
import pandas as pd

from src.models.NER.model import create_ner_model


@click.command()
@click.argument("data_input_file", type=click.Path(exists=True))
@click.argument("rules_file", type=click.Path(exists=True))
@click.argument("output_file")
def find_ner(data_input_file, rules_file: str, output_file):
    nlp = create_ner_model(rules_file)

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
