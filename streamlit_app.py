import streamlit as st
import requests
import json
from datetime import datetime
import os
import base64
from io import BytesIO
import google.generativeai as genai
import yaml
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import shutil

# Configuration
def load_config():
    try:
        with open("edjudicate_ai_app/config/config.yaml") as f:
            return yaml.safe_load(f)
    except:
        # Fallback configuration for deployment
        return {
            "gemini_api_key": st.secrets.get("GEMINI_API_KEY", "AIzaSyDT8DEp3Bzf72E9dCdrDzqUw39EDXuYn-E"),
            "models": {
                "gemini": {"model_name": "gemini-2.0-flash"},
                "embeddings": {"model_name": "all-MiniLM-L6-v2"}
            }
        }

cfg = load_config()
genai.configure(api_key=cfg["gemini_api_key"])
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize embedding model
@st.cache_resource
def get_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

embedding_model = get_embedding_model()

# Document processing functions
def load_content(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Only .pdf and .docx are supported.")

def extract_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def chunk_text(text: str, chunk_size=500, overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)

def embed_texts(texts):
    return embedding_model.encode(texts, convert_to_tensor=False).tolist()

def normalize_embeddings(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

# Session state management
def get_session_data(session_id):
    if f"session_{session_id}" not in st.session_state:
        st.session_state[f"session_{session_id}"] = {
            "index": None,
            "chunks": [],
            "vectors": None
        }
    return st.session_state[f"session_{session_id}"]

def build_index(text_chunks, session_id):
    session_data = get_session_data(session_id)
    
    vectors = embed_texts(text_chunks)
    vectors = normalize_embeddings(np.array(vectors).astype("float32"))
    
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)
    
    session_data["index"] = index
    session_data["chunks"] = text_chunks
    session_data["vectors"] = vectors
    
    return index

def retrieve_chunks(query, session_id, k=5):
    session_data = get_session_data(session_id)
    
    if session_data["index"] is None:
        return []
    
    q_vec = embed_texts([query])
    q_vec = normalize_embeddings(np.array(q_vec).astype("float32"))
    _, I = session_data["index"].search(q_vec, k)
    return [session_data["chunks"][i] for i in I[0]]

# AI reasoning
def evaluate_decision(query, session_id):
    retrieved_chunks = retrieve_chunks(query, session_id)
    clauses = "\n\n".join(retrieved_chunks)
    
    COT = """
You are a claims evaluation assistant. You are provided with:
- A customer query
- Retrieved policy document clauses

Your job is to:
1. Identify the important fields from the query (e.g., age, procedure, location, policy duration).
2. Think step-by-step to determine if the policy covers this case.
3. Reference specific clauses to justify your reasoning.
4. Give a structured JSON response with:
    - decision ("approved" or "rejected")
    - amount (if any)
    - justification

---

Query:
{query}

Retrieved Clauses:
{clauses}

---

⚠️ DO NOT return markdown, explanations, or extra text.
✅ Just return valid JSON. No triple backticks.
"""
    
    prompt = COT.format(query=query, clauses=clauses)
    response = model.generate_content(prompt)
    return response.candidates[0].content.parts[0].text

# Custom CSS for modern design
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Custom Header */
    .custom-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Neumorphic Cards */
    .neumorphic-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .neumorphic-card:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Upload Zone */
    .upload-zone {
        background: linear-gradient(145deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border: 2px dashed rgba(99, 102, 241, 0.4);
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .upload-zone:hover {
        border-color: rgba(99, 102, 241, 0.6);
        background: linear-gradient(145deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
        transform: scale(1.02);
    }
    
    .upload-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #6366f1;
    }
    
    .upload-text {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Session Badge */
    .session-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3); }
        to { box-shadow: 0 4px 25px rgba(16, 185, 129, 0.5); }
    }
    
    /* Query Input */
    .query-input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        color: #f1f5f9;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .query-input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        outline: none;
    }
    
    /* Submit Button */
    .submit-btn {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .submit-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }
    
    /* JSON Output */
    .json-output {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.2) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.9rem;
        line-height: 1.5;
        overflow-x: auto;
    }
    
    /* Clause Cards */
    .clause-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .clause-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #6366f1, #a855f7);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .clause-card:hover::before {
        opacity: 1;
    }
    
    .clause-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #6366f1;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem;
        color: #10b981;
        font-weight: 500;
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 1rem;
        color: #ef4444;
        font-weight: 500;
    }
    
    /* Hide default Streamlit elements */
    .stDeployButton { display: none; }
    .stApp > header { display: none; }
    .stApp > footer { display: none; }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #4f46e5, #9333ea);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize CSS
load_css()

# Page Configuration
st.set_page_config(
    page_title="EdjudicateAI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Header
st.markdown("""
<div class="custom-header">
    <div class="header-title">🧠 Edjudicate AI</div>
    <div class="header-subtitle">Your Intelligent Policy Document Analyzer</div>
</div>
""", unsafe_allow_html=True)

# Upload Section
st.markdown("""
<div class="neumorphic-card">
    <div class="section-header">
        📤 Upload Documents
    </div>
""", unsafe_allow_html=True)

# File Uploader with custom styling
uploaded_files = st.file_uploader(
    "Choose files",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📎</div>
        <div class="upload-text">Files uploaded successfully!</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Process files
    with st.spinner("🔄 Processing and indexing documents..."):
        all_text_chunks = []
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for uploaded_file in uploaded_files:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                raw_text = load_content(tmp_file_path)
                text_chunks = chunk_text(raw_text)
                all_text_chunks.extend(text_chunks)
            finally:
                os.unlink(tmp_file_path)  # Clean up temp file
        
        # Build index
        if all_text_chunks:
            build_index(all_text_chunks, session_id)
            st.session_state["session_id"] = session_id
            
            st.markdown(f"""
            <div class="success-message">
                ✅ Successfully processed {len(uploaded_files)} file(s) and indexed {len(all_text_chunks)} text chunks!
            </div>
            """, unsafe_allow_html=True)
            
            # Session Badge
            st.markdown(f"""
            <div style="margin: 1rem 0;">
                <span class="session-badge">
                    🗂️ Session ID: {session_id}
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-message">
                ❌ No text content could be extracted from the uploaded files.
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Query Section
st.markdown("""
<div class="neumorphic-card">
    <div class="section-header">
        🔍 Ask a Question
    </div>
""", unsafe_allow_html=True)

# Query Input
query = st.text_input(
    "Enter your question about the uploaded documents...",
    placeholder="e.g., Is cataract surgery covered? What is my deductible?",
    label_visibility="collapsed"
)

# Submit Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit_button = st.button("🚀 Submit Query", use_container_width=True)

if submit_button and query:
    session_id = st.session_state.get("session_id")
    
    if not session_id:
        st.markdown("""
        <div class="error-message">
            ⚠️ No documents uploaded yet. Please upload documents first.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Loading state
        with st.spinner("🤖 Thinking with AI..."):
            try:
                answer = evaluate_decision(query, session_id)
                relevant_chunks = retrieve_chunks(query, session_id, k=5)
                
                # AI Answer Section
                st.markdown("""
                <div class="section-header" style="margin-top: 2rem;">
                    🤖 AI Answer
                </div>
                """, unsafe_allow_html=True)
                
                # Display query
                st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <strong style="color: #94a3b8;">Q:</strong> {query}
                </div>
                """, unsafe_allow_html=True)
                
                # JSON Response
                try:
                    parsed = json.loads(answer)
                    st.markdown("""
                    <div class="json-output">
                    """, unsafe_allow_html=True)
                    st.json(parsed)
                    st.markdown("</div>", unsafe_allow_html=True)
                except json.JSONDecodeError:
                    st.markdown("""
                    <div class="json-output">
                    """, unsafe_allow_html=True)
                    st.code(answer, language="json")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Referenced Clauses
                if relevant_chunks:
                    st.markdown("""
                    <div class="section-header" style="margin-top: 2rem;">
                        📋 Referenced Clauses
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for i, clause in enumerate(relevant_chunks):
                        st.markdown(f"""
                        <div class="clause-card">
                            <div style="font-weight: 600; color: #6366f1; margin-bottom: 0.5rem;">
                                📄 Clause {i+1}
                            </div>
                            <div style="color: #e2e8f0; line-height: 1.6;">
                                {clause}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    ❌ Error: {str(e)}
                </div>
                """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='position: fixed; bottom: 20px; right: 20px; color: #64748b; font-size: 0.8rem; font-weight: 500;'>
    Powered by Edjudicate AI
</div>
""", unsafe_allow_html=True)

