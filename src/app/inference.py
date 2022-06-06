from gettext import find
from http.client import HTTPException
import os
import pandas as pd
import mlflow
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from spacy import Language
from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository

# from src.models.NER.expand_model import expand_model

load_dotenv()


app = FastAPI()

os.environ['MLFLOW_S3_ENDPOINT_URL'] = os.getenv('MLFLOW_S3_ENDPOINT_URL')


def simplify_multiple(objects):
    for obj in objects:
        if obj['brand'].find(',') > -1:
            arr = [obj | {"brand": x} for x in obj['brand'].split(',')]
            return simplify_multiple(arr)
        
        if obj['model'].find(',') > -1:
            arr = [obj | {"model": x}  for x in obj['model'].split(',')]
            return simplify_multiple(arr)
        
        if obj['year'].find(',') > -1:
            arr = [obj | {"year": x}  for x in obj['year'].split(',')]
            return simplify_multiple(arr)
    return objects

def flatten(xss):
    return [x for xs in xss for x in xs]

class Model:
    def __init__(self, model_name, model_stage) -> None:
        client = mlflow.tracking.MlflowClient()
        models = client.get_registered_model(model_name)
        model = next(x for x in models.latest_versions if x.current_stage == 'Staging')
        run_id=model.run_id

        # делаю жестюгу, потому как spacy не умеет упаковывать свои компоненты.... =((
        client = mlflow.tracking.MlflowClient()
        local_dir = os.path.abspath(os.getcwd()) + "/tmp/artifact_downloads"
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        local_path = client.download_artifacts(run_id, "expand_model.py", local_dir)
        exec(open(local_path).read())

        self.model = mlflow.spacy.load_model(model_uri=f'models:/{model_name}/{model_stage}')

    def predict(self, data):
        result = []
        for index, row in data.iterrows():
            doc = self.model(str(row['text']))
            result = result + simplify_multiple([{
                "id": index,
                "brand": doc.user_data['brands'],
                "model": doc.user_data['models'],
                "year": doc.user_data['years'],
            }])
        return  result

    
model = Model('autostat_ner', 'staging')

@app.post('/invacation')
async def create_upload_file(file: UploadFile):
    if file.filename.endswith(".csv"):
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        data = pd.read_csv(file.filename, index_col='id')
        os.remove(file.filename)

        json_compatible_item_data = jsonable_encoder(model.predict(data))
        return JSONResponse(content=json_compatible_item_data)
    else:
        raise HTTPException(status_code=400, detail="invalid file format")
    
if os.getenv('AWS_ACCESS_KEY_ID') is None or os.getenv('AWS_SECRET_ACCESS_KEY') is None:
    exit(1)