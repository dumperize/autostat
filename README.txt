snakemake --cores all -R add_ner  
uvicorn src.app.inference:app --host 0.0.0.0 --port 5040  

docker build -f Docker/fast_api/Dockerfile -t fast_api .     