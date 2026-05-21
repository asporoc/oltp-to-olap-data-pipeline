from fastapi import FastAPI

from src.pipeline.metadata.runs import get_runs, get_run_by_id
from src.pipeline.pipeline_run.run import run_pipeline

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/runs")
def start_run():
    result = run_pipeline()
    return result

@app.get("/runs/all")
def list_runs():
    result = get_runs()
    return result

@app.get("/runs/{run_id}")
def get_run(run_id: int):
    return get_run_by_id(run_id)