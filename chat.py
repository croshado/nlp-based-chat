import streamlit as st
import spacy
from sentence_transformers import SentenceTransformer, util
import json

# Load NLP model
nlp = SentenceTransformer('all-MiniLM-L6-v2')

# Load knowledge base
with open('clat_kb.json') as f:
    kb = json.load(f)

# Embed all questions from KB
kb_questions = [item['question'] for item in kb]
kb_embeddings = nlp.encode(kb_questions, convert_to_tensor=True)

# Streamlit UI
st.title("CLAT 2025 Chatbot")

user_query = st.text_input("Ask a question about CLAT:")

if user_query:
    query_embedding = nlp.encode(user_query, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, kb_embeddings)[0]
    best_match_idx = scores.argmax().item()
    answer = kb[best_match_idx]['answer']
    st.success(answer)
