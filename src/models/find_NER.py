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


class NerModel(mlflow.pyfunc.PythonModel):
    def __init__(self, model_name):         
        self.model_name = model_name

    def load_context(self, context):
        self.model = mlflow.spacy.load_model(model_uri=context.artifacts[self.model_name])

    def predict(self, context, model_input):
        dictionary = {}
        for entity in model_input.values:
            article = str(entity['text'])
            doc = self.model(article)
            dictionary[entity['id']] = doc.user_data
        
        return dictionary



@click.command()
@click.argument("data_input_file", type=click.Path(exists=True))
@click.argument("rules_file", type=click.Path(exists=True))
@click.argument("output_file")
def find_ner(data_input_file, rules_file: str, output_file):
    with mlflow.start_run(run_name='autostat_ner'):
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

        signature = infer_signature(df['vehicleproperty_description_short'], df['brands'])

        mlflow.set_tag('model_flavor', 'spacy')
        mlflow.spacy.log_model(
            spacy_model=nlp, 
            artifact_path='model',
            registered_model_name="autostat_ner", 
            signature=signature)

        # mlflow.pyfunc.save_model(
        #     path="test2", 
        #     python_model=NerModel("spacy"))
        mlflow.log_artifact('requirements.txt')

        mlflow.log_metric('count brands', df.count()['brands'])
        mlflow.log_metric('count models', df.count()['models'])
        mlflow.log_metric('count years', df.count()['years'])

 


if __name__ == "__main__":
    find_ner()
