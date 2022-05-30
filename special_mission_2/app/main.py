from fastapi import FastAPI, UploadFile, File
from fastapi.param_functions import Depends
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List, Union, Optional, Dict, Any
from datetime import datetime
from app.model import mrc_load_pipeline
from fastapi.responses import JSONResponse
from fastapi import HTTPException

app = FastAPI()

class Pipeline(BaseModel):
    name: str
    pipeline: Any


class CreatePipelineIn(BaseModel):
    model_name: str


class Input(BaseModel):
    model_name: str 
    question: str 
    context: str


class Output(BaseModel):
    model_name: str
    answer: str 


pipelines: List[Pipeline] = []


def get_pipeline(model_name):
    for pipeline_ in pipelines:
        if pipeline_.name == model_name:
            return pipeline_
    return None


@app.get("/")
def hello_world():
    return {"hello": "world"}


@app.get("/pipeline/")
def get_models():
    if not pipelines:
        return JSONResponse({'pipelines':[]})
    else:
        return JSONResponse({'pipelines':[pipeline_.name for pipeline_ in pipelines]})


@app.post("/pipeline/")
async def initialize_pipeline(new_pipeline: CreatePipelineIn) -> str:
    pipeline_names = set([pipeline_.name for pipeline_ in pipelines])

    if new_pipeline.model_name in pipeline_names:
        return JSONResponse({'model_name': new_pipeline.model_name})
    else:
        try:
            mrc_pipeline = mrc_load_pipeline(new_pipeline.model_name)
            pydantic_mrc_pipeline = Pipeline(name=new_pipeline.model_name, pipeline=mrc_pipeline)
            pipelines.append(pydantic_mrc_pipeline)
            return JSONResponse({'model_name': pydantic_mrc_pipeline.name})
        except:
            raise HTTPException(status_code=404, detail='올바른 모델을 입력해 주세요')


@app.post("/pipeline/analyze/")
def analyze(input: Input) -> Output:
    cur_pipeline = get_pipeline(input.model_name)
    if not cur_pipeline:
        raise HTTPException(status_code=404, detail='해당 모델이 활성화 되어있지 않습니다.')

    result = cur_pipeline.pipeline(question=input.question, context=input.context)
    answer = result['answer']
    output = Output(model_name = input.model_name, answer=answer)
    return output


