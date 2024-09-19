import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic

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
# for URLs
st.sidebar.header("Input URLs")
url1 = st.sidebar.text_input("Enter first URL", "")
url2 = st.sidebar.text_input("Enter second URL", "")

# for LLMs
st.sidebar.header("Select LLM")
llm_option = st.sidebar.selectbox(
    "Choose an LLM to use:",
    ("OpenAI GPT-4", "OpenAI GPT-3.5", "Claude", "Google Gemini")
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

# Secrets for API keys
openai_api_key = st.secrets.get("openai_api_key", None)
claude_api_key = st.secrets.get("claude_key", None)
google_api_key = st.secrets.get("gemini_key", None)

# Model selection logic
if llm_option == "OpenAI GPT-4":
    selected_model = "gpt-4"
elif llm_option == "OpenAI GPT-3.5":
    selected_model = "gpt-3.5-turbo"
elif llm_option == "Claude":
    selected_model = "claude-1"
else:
    selected_model = "gemini-1"

# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Memory instruction setup
def get_memory_instruction(memory_type):
    if memory_type == "Buffer of 5 questions":
        return "Buffer of 5 questions"
    elif memory_type == "Buffer of 5000 tokens":
        return "Buffer of 5000 tokens"
    else:
        return "Conversation Summary"

# Generate response based on selected LLM
def generate_llm_response(llm_option, selected_model, messages):
    response_text = ""
    if llm_option.startswith("OpenAI"):
        openai.api_key = openai_api_key
        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=messages
        )
        response_text = response['choices'][0]['message']['content']
    elif llm_option == "Claude":
        client = Anthropic(api_key=claude_api_key)
        response = client.completions.create(
            model=selected_model,
            prompt=f"\n\nHuman: {messages[0]['content']}\n\nAssistant:",
            max_tokens_to_sample=1000
        )
        response_text = response['completion']
    elif llm_option == "Google Gemini":
        # Example placeholder for Google Gemini API call
        response_text = "Google Gemini response coming soon!"
    return response_text

# Handle user input and API calls
if url1:
    document = read_url_content(url1)
    if not document:
        st.error("Could not retrieve information from URL")
        st.stop()

    memory_instruction = get_memory_instruction(memory_type)

    # User message to LLM
    user_message = {
        "role": "user",
        "content": f"Here's a document: {document} \n\n---\n\n{memory_instruction}"
    }

    messages = [user_message]

    response_text = generate_llm_response(llm_option, selected_model, messages)
    
    # Show the response
    st.write(response_text)

    # Save the user message and assistant response in session state
    st.session_state.messages.append({"role": "user", "content": document})
    st.session_state.messages.append({"role": "assistant", "content": response_text})
