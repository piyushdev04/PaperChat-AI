import streamlit as st
from pdf_parser import extract_text_from_pdf
from chunker import split_text_into_chunks
from embedder import embed_texts
from db import store_embeddings
from qa import answer_question
import tempfile
import os

st.set_page_config(page_title="Research Paper Chatbot")
st.title("🧠 Research Paper Chatbot")

if 'collection_name' not in st.session_state:
    st.session_state['collection_name'] = None
if 'chunks' not in st.session_state:
    st.session_state['chunks'] = []
if 'uploaded' not in st.session_state:
    st.session_state['uploaded'] = False

uploaded_file = st.file_uploader("Upload a research paper (PDF)", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    text = extract_text_from_pdf(tmp_path)
    os.unlink(tmp_path)
    chunks = split_text_into_chunks(text, chunk_size=500)
    embeddings = embed_texts(chunks)
    collection_name = f"paper_{hash(uploaded_file.name)}"
    store_embeddings(chunks, embeddings, collection_name)
    st.session_state['collection_name'] = collection_name
    st.session_state['chunks'] = chunks
    st.session_state['uploaded'] = True
    st.success("PDF processed and indexed!")

if st.session_state['uploaded'] and st.session_state['collection_name']:
    st.header("Ask questions about the paper:")
    question = st.text_input("Your question:")
    if st.button("Ask") and question:
        with st.spinner("Thinking..."):
            answer = answer_question(question, st.session_state['collection_name'])
        st.markdown(f"**Answer:** {answer}") 