import streamlit as st
from rag import load_and_chunk_pdf, create_vector_store, get_relevant_chunks, get_answer
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="DocMind AI",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: #0a0a0f;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.hero {
    text-align: center;
    padding: 3rem 0 2rem 0;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.hero p {
    color: #6b7280;
    font-size: 1.1rem;
    margin: 0;
}

[data-testid="stFileUploader"] {
    background: #13131a;
    border: 1.5px dashed #2d2d3d;
    border-radius: 16px;
    padding: 1.5rem;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #7c3aed;
}
            
            /* Make spinner text bright */
[data-testid="stSpinner"] p {
    color: #ffffff !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
}

/* Make success message bright */
.stSuccess {
    background: rgba(167, 139, 250, 0.15) !important;
    border: 1px solid rgba(167, 139, 250, 0.3) !important;
    color: #ffffff !important;
}

.stSuccess p {
    color: #ffffff !important;
    font-weight: 500 !important;
}

.doc-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #13131a;
    border: 1px solid #2d2d3d;
    border-radius: 100px;
    padding: 0.4rem 1rem;
    color: #a78bfa;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 1.5rem;
}

[data-testid="stChatMessage"] {
    background: #13131a !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 16px !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 0.75rem !important;
}

[data-testid="stChatMessage"] p {
    color: #ffffff !important;
    font-size: 0.97rem !important;
    line-height: 1.7 !important;
}

[data-testid="stChatMessage"] * {
    color: #ffffff !important;
}

[data-testid="stChatInput"] {
    background: #13131a !important;
    border: 1.5px solid #2d2d3d !important;
    border-radius: 14px !important;
    color: #ffffff !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
}

[data-testid="stExpander"] {
    background: #0f0f18 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 12px !important;
    margin-top: 0.5rem !important;
}
[data-testid="stExpander"] summary {
    color: #6b7280 !important;
    font-size: 0.82rem !important;
}

.source-chunk {
    background: #1a1a2e;
    border-left: 3px solid #7c3aed;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #9ca3af;
    font-size: 0.83rem;
    line-height: 1.6;
    margin-bottom: 0.5rem;
}

.stButton button {
    background: #13131a !important;
    border: 1px solid #2d2d3d !important;
    color: #9ca3af !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
}
.stButton button:hover {
    border-color: #7c3aed !important;
    color: #a78bfa !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2d2d3d; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# Sidebar — keep empty or remove
with st.sidebar:
    st.markdown("### DocMind AI")


# Init state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

# Hero
st.markdown("""
<div class="hero">
    <h1>🧠 DocMind AI</h1>
    <p>Drop a PDF. Ask anything. Get instant answers.</p>
</div>
""", unsafe_allow_html=True)

# Upload
uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

if uploaded_file and uploaded_file.name != st.session_state.pdf_name:
    st.session_state.pdf_name = uploaded_file.name
    st.session_state.messages = []
    st.session_state.vector_store = None

    with st.spinner("⚡ Processing your PDF — please wait..."):
        chunks = load_and_chunk_pdf(uploaded_file)
        st.session_state.vector_store = create_vector_store(chunks)


# Doc badge

if st.session_state.pdf_name:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="doc-badge">📄 {st.session_state.pdf_name}</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# Chat
if st.session_state.vector_store:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🧠"):
            st.write(msg["content"])

    question = st.chat_input("Ask anything about your document...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user", avatar="👤"):
            st.write(question)

        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("🧠 Thinking..."):
                context, sources = get_relevant_chunks(st.session_state.vector_store, question)
                answer = get_answer(context, question)
                st.write(answer)

                with st.expander("view sources"):
                    for i, source in enumerate(sources):
                        st.markdown(f'<div class="source-chunk"><strong>Chunk {i+1}</strong><br>{source}</div>', unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": answer})

else:
    st.markdown("""
        <div style="
            background: #13131a;
            border: 2px dashed #2d2d3d;
            border-radius: 16px;
            padding: 3rem;
            text-align: center;
            margin-top: 1rem;
        ">
            <h3 style="color: #a78bfa; margin-bottom: 0.5rem;">📂 Upload a PDF to get started</h3>
            <p style="color: #4b5563; margin: 0;">Supports any PDF — research papers, books, reports, contracts</p>
        </div>
    """, unsafe_allow_html=True)