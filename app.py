import streamlit as st
import numpy as np
import chromadb
from pypdf import PdfReader
from google import genai
from google.genai import types


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Chat With Your Documents",
    page_icon="📚",
    layout="centered"
)


# ==================================================
# TITLE
# ==================================================

st.title("📚 Chat With Your Documents")
st.caption("RAG-powered document question answering")


# ==================================================
# GEMINI API
# ==================================================

API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)


# ==================================================
# CHROMA VECTOR DATABASE
# ==================================================

if "chroma_client" not in st.session_state:

    st.session_state.chroma_client = chromadb.Client()

    st.session_state.collection = (
        st.session_state.chroma_client
        .get_or_create_collection(
            name="document_collection"
        )
    )


collection = st.session_state.collection


# ==================================================
# EXTRACT TEXT FROM DOCUMENT
# ==================================================

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


# ==================================================
# TEXT CHUNKING
# ==================================================

def create_chunks(
    text,
    chunk_size=1000,
    overlap=200
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                chunk.strip()
            )

        start += chunk_size - overlap

    return chunks


# ==================================================
# CREATE GEMINI EMBEDDING
# ==================================================

def create_embedding(text):

    result = client.models.embed_content(

        model="gemini-embedding-2",

        contents=text,

        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values


# ==================================================
# DOCUMENT UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "📄 Upload a PDF or TXT document",
    type=["pdf", "txt"]
)


if uploaded_file:

    # ------------------------------------------------
    # Detect new document
    # ------------------------------------------------

    file_id = (
        uploaded_file.name,
        uploaded_file.size
    )

    if (
        "current_file" not in st.session_state
        or
        st.session_state.current_file != file_id
    ):

        # Store current file
        st.session_state.current_file = file_id

        # Clear old vectors
        try:

            st.session_state.chroma_client.delete_collection(
                name="document_collection"
            )

        except Exception:
            pass

        # Create fresh collection
        st.session_state.collection = (
            st.session_state.chroma_client
            .get_or_create_collection(
                name="document_collection"
            )
        )

        collection = st.session_state.collection

        # Extract text
        document_text = extract_text(
            uploaded_file
        )

        if not document_text.strip():

            st.error(
                "❌ Could not extract text from this document."
            )

            st.stop()

        # Create chunks
        chunks = create_chunks(
            document_text
        )

        st.session_state.chunks = chunks

        st.success(
            f"📄 Uploaded: {uploaded_file.name}"
        )

        st.success(
            f"✅ Document processed into {len(chunks)} chunks."
        )

        # ------------------------------------------------
        # Create embeddings
        # ------------------------------------------------

        with st.spinner(
            "🧠 Creating document embeddings..."
        ):

            embeddings = []

            for chunk in chunks:

                embedding = create_embedding(
                    chunk
                )

                embeddings.append(
                    embedding
                )

        # ------------------------------------------------
        # Store embeddings in ChromaDB
        # ------------------------------------------------

        with st.spinner(
            "🗄️ Storing vectors in ChromaDB..."
        ):

            ids = [
                f"chunk_{i}"
                for i in range(len(chunks))
            ]

            collection.add(

                ids=ids,

                documents=chunks,

                embeddings=embeddings
            )

        st.success(
            "✅ Embeddings stored in ChromaDB!"
        )

        st.info(
            f"🗄️ Vector database contains "
            f"{collection.count()} document chunks."
        )


# ==================================================
# QUESTION ANSWERING
# ==================================================

if uploaded_file:

    question = st.text_input(
        "💬 Ask a question about your document"
    )

    if question:

        # ------------------------------------------------
        # Create question embedding
        # ------------------------------------------------

        with st.spinner(
            "🔎 Searching the vector database..."
        ):

            question_embedding = create_embedding(
                question
            )

            # ------------------------------------------------
            # Retrieve relevant chunks
            # ------------------------------------------------

            results = collection.query(

                query_embeddings=[
                    question_embedding
                ],

                n_results=min(
                    3,
                    collection.count()
                )
            )

            retrieved_chunks = (
                results["documents"][0]
            )

            context = "\n\n".join(
                retrieved_chunks
            )


        # ------------------------------------------------
        # Show retrieved context
        # ------------------------------------------------

        with st.expander(
            "🔎 Retrieved Document Context"
        ):

            for i, chunk in enumerate(
                retrieved_chunks,
                start=1
            ):

                st.markdown(
                    f"**Retrieved Chunk {i}**"
                )

                st.write(chunk)


        # ------------------------------------------------
        # Generate answer
        # ------------------------------------------------

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

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}
"""

            response = client.models.generate_content(

                model="gemini-3.6-flash",

                contents=prompt
            )


        # ------------------------------------------------
        # Display answer
        # ------------------------------------------------

        st.subheader("🤖 Answer")

        st.write(
            response.text
        )