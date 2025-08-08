import streamlit as st
import requests
import json
from datetime import datetime
import os
import base64
from io import BytesIO

API_URL = "http://127.0.0.1:8000"

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
    
    # Upload files
    with st.spinner("🔄 Processing and indexing documents..."):
        files_data = []
        for uploaded_file in uploaded_files:
            files_data.append(("uploaded_files", (uploaded_file.name, uploaded_file.getvalue())))
        
        response = requests.post(f"{API_URL}/upload_docs", files=files_data)

    if response.status_code == 200:
        data = response.json()
        session_id = data.get("session_id")
        st.session_state["session_id"] = session_id
            
            st.markdown(f"""
            <div class="success-message">
                ✅ {data.get("message", "Upload succeeded!")}
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
            st.markdown(f"""
            <div class="error-message">
                ❌ {response.json().get("error", "Upload failed.")}
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
            response = requests.post(
                f"{API_URL}/query",
                json={"query": query, "session_id": session_id}
            )

        if response.status_code == 200:
            result = response.json()

            if "error" in result:
                st.markdown(f"""
                <div class="error-message">
                    ❌ Error: {result["error"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                # AI Answer Section
                st.markdown("""
                <div class="section-header" style="margin-top: 2rem;">
                    🤖 AI Answer
                </div>
                """, unsafe_allow_html=True)
                
                # Display query
                st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <strong style="color: #94a3b8;">Q:</strong> {result.get('query')}
                </div>
                """, unsafe_allow_html=True)
                
                # JSON Response
                response_text = result.get("response", "")
                try:
                    parsed = json.loads(response_text)
                    st.markdown("""
                    <div class="json-output">
                    """, unsafe_allow_html=True)
                    st.json(parsed)
                    st.markdown("</div>", unsafe_allow_html=True)
                except json.JSONDecodeError:
                    st.markdown("""
                    <div class="json-output">
                    """, unsafe_allow_html=True)
                    st.code(response_text, language="json")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Referenced Clauses
                clauses = result.get("retrieved_clauses", [])
                if clauses:
                    st.markdown("""
                    <div class="section-header" style="margin-top: 2rem;">
                        📋 Referenced Clauses
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for i, clause in enumerate(clauses):
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
        else:
            try:
                error_msg = response.json().get("error", "Unknown error")
                st.markdown(f"""
                <div class="error-message">
                    ❌ Server Error: {error_msg}
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown("""
                <div class="error-message">
                    ❌ Unknown Error occurred.
                </div>
                """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='position: fixed; bottom: 20px; right: 20px; color: #64748b; font-size: 0.8rem; font-weight: 500;'>
    Powered by Edjudicate AI
    </div>
""", unsafe_allow_html=True)

