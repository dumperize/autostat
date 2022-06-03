FROM python:3.9

WORKDIR /code


RUN pip install --upgrade pip
# RUN pip install poetry

COPY ./Docker/fast_api/requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./src/app /code/app
COPY ./Docker/fast_api/.env /code/app/.env

CMD ["uvicorn", "app.inference:app", "--host", "0.0.0.0", "--port", "80"]
