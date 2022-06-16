from tqdm import tqdm
import click
import os
import pandas as pd
import mlflow
import mlflow.spacy
from mlflow.models.signature import infer_signature

from src.models.NER.model import create_ner_model


from dotenv import load_dotenv
load_dotenv()

remote_server_uri = os.getenv('MLFLOW_TRACKING_URI')
mlflow.set_tracking_uri(remote_server_uri)


@click.command()
@click.argument("data_input_file", type=click.Path(exists=True))
@click.argument("rules_file", type=click.Path(exists=True))
@click.argument("important_names_file", type=click.Path(exists=True))
@click.argument("output_file")
def find_ner(data_input_file, rules_file: str, important_names_file: str, output_file):
    with mlflow.start_run(run_name='autostat_ner'):
        nlp = create_ner_model(rules_file, important_names_file)

        df = pd.read_csv(data_input_file, delimiter='|')
        # df = df[:10]
        ents_info = []
        
        for article in tqdm(df['vehicleproperty_description_short']):
            article = str(article)
            doc = nlp(article)
            ents_info.append(doc.user_data)

        ents_info_df = pd.DataFrame.from_records(ents_info)
        df.index.name = 'order'
        df = df.join(ents_info_df,on='order') 
        df.to_excel(output_file, index=False, encoding='utf-8')

        signature = infer_signature(df['vehicleproperty_description_short'], df['brands'])

        mlflow.set_tag('model_flavor', 'spacy')
        mlflow.spacy.log_model(
            spacy_model=nlp, 
            artifact_path='model',
            registered_model_name="autostat_ner", 
            signature=signature)

        mlflow.log_artifact(rules_file)
        mlflow.log_artifact(important_names_file)

        mlflow.log_metric('count brands', df.count()['brands'])
        mlflow.log_metric('count models', df.count()['models'])
        mlflow.log_metric('count years', df.count()['years'])

 
if __name__ == "__main__":
    find_ner()
