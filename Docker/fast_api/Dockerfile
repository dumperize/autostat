FROM python:3.9

WORKDIR /code


RUN pip3 install --upgrade pip
# RUN pip install poetry

COPY ./Docker/fast_api/requirements.txt /code/
RUN pip3 install -r requirements.txt

COPY ./src/app /code/app
COPY ./src/models/NER /code/src/models/NER
COPY ./data/raw/brand_with_models/ /code/data/raw/brand_with_models/
COPY ./Docker/fast_api/.env /code/app/.env

CMD ["uvicorn", "app.inference:app", "--host", "0.0.0.0", "--port", "8003"]
