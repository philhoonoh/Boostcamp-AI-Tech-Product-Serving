import io
import os
from pathlib import Path

import requests
from PIL import Image

import streamlit as st
from app.confirm_button_hack import cache_on_button_press
import copy

# SETTING PAGE CONFIG TO WIDE MODE
ASSETS_DIR_PATH = os.path.join(Path(__file__).parent.parent.parent.parent, "assets")

st.set_page_config(layout="wide")

root_password = 'password'


def main():
    st.title("HuggingFace Transformer MRC Models")
    st.write('HuggingFace Transformer MRC Models 예시')
    model_1 = "bespin-global/klue-bert-base-aihub-mrc"
    model_2 = "ainize/klue-bert-base-mrc"
    st.write(f'예1. {model_1}')
    st.write(f'예2. {model_2}')
    model_name = st.text_input("HuggingFace Transformer MRC 모델을 입력해주세요")

    if model_name:
        response = requests.post("http://localhost:8001/pipeline", json = {'model_name' : model_name})
        st.write(f"{response.json()['model_name']} 를 시작합니다")
        response = requests.get("http://localhost:8001/pipeline")
        st.write(f"현재 {response.json()['pipelines']} 이 활성화 되어 있습니다.")

        model_select = st.text_input("활성화된 모델 중 하나를 택해주세요")
        question_input = st.text_input("질문를 입력해주세요")
        context_input = st.text_input("텍스트를 입력해주세요")

        data_json = {
            'model_name' : model_select,
            'question': question_input,
            'context': context_input
        }

        if model_select and question_input and context_input:
            response = requests.post("http://localhost:8001/pipeline/analyze/", json = data_json)
            model_name = response.json()["model_name"]
            answer = response.json()["answer"]
            st.write(f'Model : {model_name}  \n Answer : {answer}')


@cache_on_button_press('Authenticate')
def authenticate(password) -> bool:
    return password == root_password


password = st.text_input('password', type="password")

if authenticate(password):
    st.success('You are authenticated!')
    main()
else:
    st.error('The password is invalid.')
