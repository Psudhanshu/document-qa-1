import streamlit as st
from openai import OpenAI
import openai
import requests
from bs4 import BeautifulSoup
# Title of the app
st.title("Chatbot")

# Function to read the content of a URL
def read_url_content(url, max_chars=3000):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        return text[:max_chars]
    except requests.RequestException as e:
        st.error(f"Error reading {url}: {e}")
        return None

# Sidebar
# for urls
st.sidebar.header("Input URLs")
url1 = st.sidebar.text_input("Enter first URL", "")
url2 = st.sidebar.text_input("Enter 2nd URL", "")
# for llms
st.sidebar.header("Select LLM")
llm_option = st.sidebar.selectbox(
    "Choose an LLM to use:",
    ("OpenAI GPT 4o", "OpenAI GPT 3.5","Cohere Command", "Google Gemini")
)
# for memory type selection
memory_type = st.sidebar.selectbox(
    "Choose the type of conversation memory to use:",
    (
        "Buffer of 5 questions",
        "Conversation summary",
        "Buffer of 5000 tokens"
    )
)
# secrets client
openai_api_key = st.secrets.get("open_api_key",None)
if llm_option == "OpenAI (GPT-3.5-turbo or GPT-4)":
    selected_model = "gpt-4"
else:
    selected_model = "gpt-3.5-turbo"

# choose models


# Initialize the messages list if not already in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
url_input = st.text_input(url1,url2)

if url_input:
    document = read_url_content(url_input)
    if not document:
        st.error("Could not retrive information from URL")
        st.stop()
    
    # prompt engg
    if memory_type == "Buffer of 5 questions":
        memory_instruction = f"Buffer of 5 questions"
    elif memory_type == "Buffer of 5000 tokens":
        memory_instruction = f"Buffer of 5000 tokens"
    else:
        memory_instruction = f"Conversation Summary"
    
    # messages 
    messages = [
        {
            "role":"user",
            "content":f"Here's a document: {document} \n\n---\n\n{memory_instruction}",
        }
    ]
    
    # generating answer using given api
    client = OpenAI(api_key=openai_api_key)
    stream = client.chat.completions.create(
        model = selected_model,
        messages = messages,
        stream = True,
    )
    # stream the response
    st.write_stream(stream)
   
   