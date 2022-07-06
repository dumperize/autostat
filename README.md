# autostat

```
install docker
install docker-compose
```

залогинится в докере
```
docker login
```

snakemake пока тоже нужен инсталим его - https://snakemake.readthedocs.io/en/stable/getting_started/installation.html

TODO потом заменить на DVC


все еще нужно прописать
`export PYTHONPATH="${PYTHONPATH}:path/to/project"`
TODO вынести  

собрать mlflow
```
docker build -f Docker/mlflow_image/Dockerfile  -t mlflow_server .
```

собрать fast_api
```
docker build -f Docker/fast_api/Dockerfile -t fast_api .    
```

запустить докер
```
docker-compose up -d --build          
```


заметочки
```
snakemake --cores all -R add_ner  
uvicorn src.app.inference:app --host 0.0.0.0 --port 5040    
```
