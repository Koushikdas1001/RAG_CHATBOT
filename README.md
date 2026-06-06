# 🧠 DocMind AI — RAG Chatbot

Chat with any PDF using AI. Upload a document and ask
questions — get accurate answers with source references.

## 🔗 Live Demo
[View Live App](https://your-app.streamlit.app)

## ✨ Features
- Upload any PDF document
- AI-powered answers using RAG pipeline
- Shows source chunks for every answer
- Beautiful dark UI
- Chat history with clear option

## 🛠 How it works
1. PDF is split into 500-character chunks
2. Chunks converted to embeddings using HuggingFace
3. Stored in FAISS vector database for fast similarity search
4. Question matched to relevant chunks
5. Groq AI (LLaMA 3.3) answers from those chunks

## 🔧 Tech Stack
- Python • Streamlit • Groq AI • LLaMA 3.3
- LangChain • FAISS • HuggingFace • PyPDF2

## 🚀 Run Locally
1. Clone the repo
2. pip install -r requirements.txt
3. Add GROQ_API_KEY to .env
4. streamlit run app.py