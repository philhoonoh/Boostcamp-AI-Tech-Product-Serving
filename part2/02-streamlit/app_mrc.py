import streamlit as st
import time
from transformers import pipeline
import copy
import tokenizers
import os
from predict import load_model, get_prediction
from confirm_button_hack import cache_on_button_press

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

root_password = 'password'



@st.cache(hash_funcs={tokenizers.Tokenizer: lambda _: None, tokenizers.AddedToken: lambda _: None})
def mrc_load_model(model_name) -> pipeline:
    mrc_pipeline = pipeline(task="question-answering", model=model_name)
    return mrc_pipeline

def main():
    st.title("MRC Model")
    st.write('Input the huggingface MRC model ')
    st.write('jihji/koelectra-base-klue-mrc')
    st.write('ainize/klue-bert-base-mrc')
    
    model_input = st.text_input("위의 모델 중 하나를 입력해주세요")
    
    if model_input:
        mrc_pipeline = copy.deepcopy(mrc_load_model(model_input))
        
    question_input = st.text_input("질문를 입력해주세요")
    context_input = st.text_input("텍스트를 입력해주세요")
    
    if question_input and context_input:
        result = mrc_pipeline(question=question_input, context=context_input)
        st.write(f"Answer is {result['answer']}")


@cache_on_button_press('Authenticate')
def authenticate(password) -> bool:
    print(type(password))
    return password == root_password


password = st.text_input('password', type="password")

if authenticate(password):
    st.success('You are authenticated!')
    main()
else:
    st.error('The password is invalid.')