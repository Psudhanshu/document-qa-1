import os
import faiss
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Function to read HTML files and extract text
def extract_text_from_html(file_path):
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()

# Create a vector database
def create_vector_db(directory):
    documents = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            text = extract_text_from_html(os.path.join(directory, filename))
            documents.append(text)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents).toarray().astype('float32')

    # Create the FAISS index
    index = faiss.IndexFlatL2(X.shape[1])
    index.add(X)

    # Save the index and vectorizer
    faiss.write_index(index, 'vector_db.index')
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)

# Check if the vector DB exists, if not, create it
if not os.path.exists('vector_db.index'):
    create_vector_db('path/to/html/files')
