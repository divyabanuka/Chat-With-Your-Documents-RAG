# 📚 Chat With Your Documents — RAG Application

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF or TXT documents and ask questions about their content using Gemini, embeddings, ChromaDB, and Streamlit.

## 🚀 Live Demo

https://chat-with-your-documents-rag-pfi2e3qtyscaqywsv2u4op.streamlit.app/

## 📌 Project Overview

This project demonstrates a practical Retrieval-Augmented Generation (RAG) system for document question answering.

The application allows users to upload a PDF or TXT document and ask questions about its content. The system retrieves relevant information from the document and uses Gemini to generate an answer based on the retrieved context.

## 🔄 RAG Pipeline

Document → Text Extraction → Chunking → Embeddings → ChromaDB → Retrieval → Gemini → Answer

## ✨ Features

- 📄 Upload PDF and TXT documents
- ✂️ Automatic text chunking
- 🧠 Gemini-powered embeddings
- 🗄️ ChromaDB vector database
- 🔎 Semantic document retrieval
- 🤖 Gemini-powered question answering
- 📚 Display retrieved document context
- 🌐 Streamlit web application
- 🔐 Secure API key management using Streamlit Secrets

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google GenAI Python SDK
- Gemini Embeddings
- ChromaDB
- PyPDF
- NumPy

## 🧠 How It Works

1. Document Upload
   The user uploads a PDF or TXT document.

2. Text Extraction
   Text is extracted from the uploaded document.

3. Text Chunking
   The extracted text is divided into smaller overlapping chunks.

4. Embeddings
   Each document chunk is converted into a numerical vector using Gemini embeddings.

5. Vector Database
   The embeddings and document chunks are stored in ChromaDB.

6. Question Embedding
   The user's question is converted into an embedding.

7. Retrieval
   ChromaDB retrieves the most relevant document chunks.

8. LLM Generation
   The retrieved context and question are sent to Gemini.

9. Final Answer
   Gemini generates an answer using the retrieved document context.

## 📊 Architecture

📄 PDF / TXT Document
        ↓
📖 Text Extraction
        ↓
✂️ Text Chunking
        ↓
🧠 Gemini Embeddings
        ↓
🗄️ ChromaDB Vector Database
        ↓
🔎 Similarity Search
        ↓
📚 Relevant Document Chunks
        ↓
🤖 Gemini LLM
        ↓
💬 Final Answer


## ⚙️ Installation

Clone the repository:

git clone https://github.com/divyabanuka/Chat-With-Your-Documents-RAG.git

Open the project directory:

cd Chat-With-Your-Documents-RAG

Install the required packages:

pip install -r requirements.txt

Run the application:

streamlit run app.py

## 🔑 API Configuration

This project uses the Google Gemini API.

For local development, configure the Gemini API key using Streamlit Secrets.

Create:

.streamlit/secrets.toml

Add:

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

Never upload your API key to GitHub.

For Streamlit Cloud deployment, add the API key through the application's Secrets settings.

## 💡 How to Use

1. Open the live application.
2. Upload a PDF or TXT document.
3. Wait for the document to be processed.
4. The application creates text chunks.
5. Gemini embeddings are generated.
6. Embeddings are stored in ChromaDB.
7. Enter a question about the document.
8. The system retrieves relevant document chunks.
9. Gemini generates an answer using the retrieved context.
10. Retrieved context can be viewed in the application.

## 🧪 Example

Document:
Python Programming Course — Week 4 Capstone Project

Question:
What is this document about?

Result:
The application retrieves relevant sections from the document and generates an answer based on the retrieved context.

## 📸 Application Screenshots

The application demonstrates:

- Document upload
- Document processing
- Embedding generation
- ChromaDB vector storage
- Retrieved document context
- Generated answer

## 🎯 Learning Outcomes

Through this project, I learned:

- Retrieval-Augmented Generation (RAG)
- Text chunking
- Text embeddings
- Semantic similarity
- Vector databases
- ChromaDB
- Document retrieval
- Large Language Model integration
- Prompt engineering
- Streamlit application development
- Gemini API integration
- Secure API key management

## 🔮 Future Improvements

- Support multiple documents
- Add conversation history
- Add DOCX document support
- Add source and page citations
- Improve chunking strategies
- Add persistent vector storage
- Add user authentication
- Improve chat interface
- Add document management features

## 📋 Internship Module

CodoMax AI/GenAI Internship

Module 4: RAG, Embeddings & Vector Databases

Project: Chat With Your Documents

Required Pipeline:

Document → Chunking → Embeddings → Vector DB → Retrieval → LLM → Answer

## 🌐 Links

Live Application:
https://scaqyws2u4op.streamlit.app/

GitHub Repository:
https://github.com/divyabanuka/Chat-With-Your-Documents-RAG

## 👩‍💻 Author

Divya Banuka

B.Tech — Artificial Intelligence & Machine Learning

GitHub:
https://github.com/divyabanuka

## ⭐ Acknowledgement

This project was developed as part of the CodoMax AI/GenAI internship learning activities to gain practical experience with Retrieval-Augmented Generation, embeddings, vector databases, document retrieval, and large language models.

⭐ If you find this project useful, consider giving the repository a star!