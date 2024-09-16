import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Function to read the content of a URL
def read_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        st.error(f"Error reading {url}: {e}")
        return None

# Function to validate the API key for the selected LLM
def validate_api_key(model, openai_key=None, gemini_key=None):
    if model == "OpenAI (GPT-3.5-turbo or GPT-4)":
        if not openai_key:
            st.error("OpenAI API key is required to use OpenAI models.")
            return False
    elif model == "Google Gemini":
        if not gemini_key:
            st.error("Google Gemini API key is required to use Google Gemini.")
            return False
    return True

# Show title and description
st.title("📄 URL Document Summarizer")
st.write(
    "Provide a URL and ask a question – GPT or Gemini will answer! "
    "To use this app, you need to provide the appropriate API key (OpenAI or Google Gemini)."
)

# Sidebar options
st.sidebar.title("Model & Summary Options")

# Option to select LLM model from a dropdown
llm_option = st.sidebar.selectbox(
    "Select LLM model:",
    ("OpenAI (GPT-3.5-turbo or GPT-4)", "Google Gemini")
)

# Option to use advanced GPT-4 model if OpenAI is selected
use_advanced_model = st.sidebar.checkbox("Use Advanced Model (GPT-4)", disabled=(llm_option == "Google Gemini"))

# Dropdown menu to select output language
language = st.selectbox(
    "Select output language:",
    ("English", "French", "Spanish")
)

# Summary option
summary_option = st.sidebar.radio(
    "Select the type of summary you'd like:",
    (
        "Summarize in 100 words",
        "Summarize in 2 paragraphs",
        "Summarize in 5 bullet points"
    )
)

# API keys from secrets
openai_api_key = st.secrets.get("open_api_key", None)
gemini_api_key = st.secrets.get("gemini_key", None)

# Choose the model based on the selected LLM
if llm_option == "OpenAI (GPT-3.5-turbo or GPT-4)":
    selected_model = "gpt-4" if use_advanced_model else "gpt-3.5-turbo"
else:
    selected_model = "google-gemini"  # For this example, we refer to Google Gemini as 'google-gemini'

# Validate API key for the selected model
if not validate_api_key(llm_option, openai_key=openai_api_key, gemini_key=gemini_api_key):
    st.stop()  # Stop execution if no valid key is provided

# Let the user provide a URL
url_input = st.text_input("Enter a URL to extract content from")

# Ask the user for a question via `st.text_area`.
question = st.text_area(
    "Now ask a question about the URL content!",
    placeholder="Can you give me a short summary?",
    disabled=not url_input,
)

if url_input and question:

    # Process the URL content
    document = read_url_content(url_input)
    if not document:
        st.error("Could not retrieve content from the provided URL.")
        st.stop()

    # Adjust the prompt based on the selected summary option
    if summary_option == "Summarize in 100 words":
        summary_instruction = f"Summarize the document in about 100 words in {language}."
    elif summary_option == "Summarize in 2 paragraphs":
        summary_instruction = f"Summarize the document in 2 connecting paragraphs in {language}."
    else:
        summary_instruction = f"Summarize the document in 5 bullet points in {language}."

    # Prepare the message for the selected LLM
    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {summary_instruction}",
        }
    ]

    # Generate an answer using the appropriate LLM API
    if llm_option == "OpenAI (GPT-3.5-turbo or GPT-4)":
        client = OpenAI(api_key=openai_api_key)
        stream = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            stream=True,
        )
        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
    
    elif llm_option == "Google Gemini":
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello!")
        print(response.text)
    print()