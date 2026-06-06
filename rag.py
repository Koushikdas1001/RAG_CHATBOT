from groq import Groq
from dotenv import load_dotenv
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import PyPDF2

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_and_chunk_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    raw_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            raw_text += text

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(raw_text)
    return chunks

def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def get_relevant_chunks(vector_store, question, k=3):
    results = vector_store.similarity_search(question, k=k)
    context = "\n\n".join([doc.page_content for doc in results])
    sources = [doc.page_content for doc in results]
    return context, sources

def get_answer(context, question):
    prompt = f"""You are a helpful assistant that answers questions
based ONLY on the document provided below.
If the answer is not in the document, say
"I couldn't find that in the document."

DOCUMENT CONTEXT:
{context}

QUESTION:
{question}

Give a clear and concise answer based on the document."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful document assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content