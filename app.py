import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="Chat With Your Documents",
    page_icon="📚",
    layout="centered"
)

# Title
st.title("📚 Chat With Your Documents")
st.caption("RAG-powered document question answering")

# Gemini API
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# Upload document
uploaded_file = st.file_uploader(
    "📄 Upload your document",
    type=["pdf", "txt"]
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    if uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")

        st.subheader("📖 Document Preview")
        st.write(text[:2000])

    else:
        st.info("PDF uploaded successfully.")

    question = st.text_input(
        "💬 Ask a question about your document"
    )

    if question:
        st.info("Document processing will be added in the next step.")