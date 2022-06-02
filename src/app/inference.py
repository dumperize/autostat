from http.client import HTTPException
import os
import pandas as pd
import mlflow
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File

load_dotenv()


app = FastAPI()

os.environ['MLFLOW_S3_ENDPOINT_URL'] = os.getenv('MLFLOW_S3_ENDPOINT_URL')

class Model:
    def __init__(self, model_name, model_stage) -> None:
        self.model = mlflow.pyfunc.load_model(f'models:/{model_name}/{model_stage}')

    def predict(self, data):
        prediction = self.model.predict(data)
        return prediction

    
model = Model('autostat_ner', 'staging')


@app.post('invacation')
async def create_upload_file(file: UploadFile = File(...)):
    if file.filename.endswith(".csv"):
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        data = pd.read_csv(file.filename)
        os.remove(file.filename)
        return list(model.predict(data))
    else:
        raise HTTPException(status_code=400, detail="invalid file format")
    
if os.genenv('AWS_ACCESS_KEY_ID') is None or os.getenv('AWS_SECRET_ACCESS_KEY') is None:
    exit(1)