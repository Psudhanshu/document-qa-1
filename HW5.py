import streamlit as st
from openai import OpenAI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Path to the directory where your course data is stored
course_data_path = "/workspaces/document-qa-1/course_data.csv"

# Load the course data from the CSV file
def load_course_data(path):
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return None

# Load the course data
course_data = load_course_data(course_data_path)

# Ensure the data loaded successfully
if course_data is not None:
    course_names = course_data['course_name'].tolist()
    course_descriptions = course_data['course_description'].tolist()

    # Vectorize the course descriptions using TF-IDF
    vectorizer = TfidfVectorizer()
    course_vectors = vectorizer.fit_transform(course_descriptions)

    # Set up the Streamlit app
    st.title("Short-Term Memory Chatbot for Courses")

    # Function to perform vector search on the course data
    def vector_search(query, course_vectors, course_names):
        query_vec = vectorizer.transform([query])
        similarity_scores = cosine_similarity(query_vec, course_vectors).flatten()
        # Find the course with the highest similarity score
        best_match_index = similarity_scores.argmax()
        if similarity_scores[best_match_index] > 0.1:  # Threshold to find a meaningful match
            return course_names[best_match_index], similarity_scores[best_match_index]
        else:
            return None, 0

    # Initialize OpenAI API client
    def initialize_openai_client():
        return OpenAI(api_key=st.secrets["open_api_key"])

    # Create a response from the OpenAI chatbot
    def create_chatbot_response(user_input, course_name, similarity_score):
        client = initialize_openai_client()

        # Build the context with the relevant course info
        context = [
            {"role": "system", "content": f"The most relevant course based on your query is: {course_name} "
                                          f"(Similarity Score: {round(similarity_score, 2)})"},
            {"role": "user", "content": user_input}
        ]

        # Get a completion from OpenAI GPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context
        )

        return response.choices[0].message.content

    # User input for query (related to courses)
    query_input = st.text_input("Enter your question about courses:")

    if query_input:
        # Perform vector search
        best_match, similarity = vector_search(query_input, course_vectors, course_names)

        if best_match:
            st.write(f"### Best Match: {best_match} (Similarity: {similarity:.2f})")

            # User question for the chatbot
            user_query = st.text_area("Ask a follow-up question:", "What should I focus on in this course?")

            if user_query:
                with st.spinner("Generating a response..."):
                    chatbot_reply = create_chatbot_response(user_query, best_match, similarity)
                    st.write("### Chatbot Response:")
                    st.write(chatbot_reply)
        else:
            st.write("No relevant courses found for your query.")
else:
    st.error("Failed to load course data.")
