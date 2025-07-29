import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
import yaml
from lxml.html import fromstring
import requests
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)


# Helper functions
def get_source(link):
    response = requests.get(link).text
    parser = fromstring(response)
    article_content = parser.find_class("ci bh gb gc gd ge")[1]
    return article_content.text_content()




messages = [("system", CONFIG["prompt"]), ("human", "{input}")]
llm = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages(messages=messages)
chain = prompt | llm


# Callbacks
def generate_question():
    st.session_state.generated = True
    input_link = st.session_state["medium_link"]
    text = chain.invoke({"input": get_source(input_link)}).content
    print(text)
    answers = json.loads(text)
    # st.session_state.output = text.content
    st.session_state.question = answers['question']
    st.session_state.answer_1 = answers['answer_a']
    st.session_state.answer_2 = answers['answer_b']
    st.session_state.answer_3 = answers['answer_c']
    st.session_state.answer_4 = answers['answer_d']
    st.session_state.correct_answer = answers['correct_answer']


    
@st.dialog("Your answer...")
def check_answer(submission):
    if submission == st.session_state.correct_answer:
        st.title("Congrats!!🎉🎉🎉")
    else:
        st.title("booo!!💀")


# session variables
if "generated" not in st.session_state:
    st.session_state.generated = False

if "question" not in st.session_state:
    st.session_state.question = "question"

if "answer_1" not in st.session_state:
    st.session_state.answer_1 = "answer_1"

if "answer_2" not in st.session_state:
    st.session_state.answer_2 = "answer_2"

if "answer_3" not in st.session_state:
    st.session_state.answer_3 = "answer_3"

if "answer_4" not in st.session_state:
    st.session_state.answer_4 = "answer_4"

st.title("Quizz Generator 🧠")

link_input = st.text_input(
    label="Link to a Medium Article", key="medium_link"
)

generation_button = st.button('Generate Question', on_click=generate_question)

if st.session_state.generated:
    st.markdown(f"### {st.session_state.question}")
    col1, col2 = st.columns(2)

    with col1:
        if st.button(st.session_state.answer_1):
            check_answer('a')
        if st.button(st.session_state.answer_3):
            check_answer('c')

    with col2:
        if st.button(st.session_state.answer_2):
            check_answer('b')
        if st.button(st.session_state.answer_4):
            check_answer('d')