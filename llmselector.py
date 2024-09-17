import streamlit as st 
from openai import OpenAI
from langchain_openai.chat_models import ChatOpenAI

st.title("LLM selector")

client = OpenAI(api_key=st.secrets["open_api_key"])

def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=client)
    st.info(model.invoke(input_text))


with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    if not client.startswith("sk-"):
        st.warning("Please enter key")
    if submitted and client.startswith("sk-"):
        generate_response(text)

        