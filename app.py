import streamlit as st
import numpy as np
from pypdf import PdfReader
from google import genai
from google.genai import types


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Chat With Your Documents",
    page_icon="📚",
    layout="centered"
)


# ---------------- TITLE ----------------

st.title("📚 Chat With Your Documents")
st.caption("RAG-powered document question answering")


# ---------------- GEMINI API ----------------

API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)


# ---------------- TEXT EXTRACTION ----------------

def extract_text(uploaded_file):

    if uploaded_file.type == "application/pdf":

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    else:

        return uploaded_file.read().decode("utf-8")


# ---------------- TEXT CHUNKING ----------------

def create_chunks(text, chunk_size=1000, overlap=200):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


# ---------------- CREATE EMBEDDING ----------------

def create_embedding(text):

    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    return np.array(result.embeddings[0].values)


# ---------------- COSINE SIMILARITY ----------------

def cosine_similarity(a, b):

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


# ---------------- DOCUMENT UPLOAD ----------------

uploaded_file = st.file_uploader(
    "📄 Upload a PDF or TXT document",
    type=["pdf", "txt"]
)


if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    # Extract text
    document_text = extract_text(uploaded_file)

    if not document_text.strip():

        st.error(
            "❌ Could not extract text from this document."
        )

        st.stop()


    # Create chunks
    chunks = create_chunks(document_text)


    st.success(
        f"✅ Document processed into {len(chunks)} chunks."
    )


    # ---------------- CREATE DOCUMENT EMBEDDINGS ----------------

    if "embeddings" not in st.session_state:

        with st.spinner(
            "🧠 Creating document embeddings..."
        ):

            embeddings = []

            for chunk in chunks:

                embedding = create_embedding(chunk)

                embeddings.append(embedding)

            st.session_state.embeddings = embeddings
            st.session_state.chunks = chunks

        st.success(
            "✅ Embeddings created successfully!"
        )


    # ---------------- ASK QUESTION ----------------

    question = st.text_input(
        "💬 Ask a question about your document"
    )


    if question:

        with st.spinner(
            "🔎 Searching the document..."
        ):

            # Create question embedding
            question_embedding = create_embedding(
                question
            )


            # Calculate similarities
            similarities = []

            for embedding in st.session_state.embeddings:

                score = cosine_similarity(
                    question_embedding,
                    embedding
                )

                similarities.append(score)


            # Get top 3 chunks
            top_indices = np.argsort(
                similarities
            )[-3:][::-1]


            retrieved_chunks = []

            for index in top_indices:

                retrieved_chunks.append(
                    st.session_state.chunks[index]
                )


            context = "\n\n".join(
                retrieved_chunks
            )


        # ---------------- DISPLAY RETRIEVED CONTEXT ----------------

        with st.expander(
            "🔎 Retrieved Document Context"
        ):

            st.write(context)


        # ---------------- GENERATE ANSWER ----------------

        with st.spinner(
            "🤖 Generating answer..."
        ):

            prompt = f"""
You are a helpful document question-answering assistant.

Answer the user's question using ONLY the
provided document context.

If the answer cannot be found in the context,
say:

"I couldn't find the answer in the uploaded document."

Document context:

{context}

User question:

{question}
"""


            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )


        st.subheader("🤖 Answer")

        st.write(response.text)