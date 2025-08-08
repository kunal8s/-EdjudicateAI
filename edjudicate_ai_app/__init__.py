"""
Edjudicate AI - Intelligent Policy Document Analyzer

A modern AI-powered application for analyzing and explaining insurance policy documents
using semantic search and LLM reasoning.
"""

__version__ = "0.1.0"
__author__ = "Edjudicate AI Team"
__description__ = "Intelligent Policy Document Analyzer"

# Import main components for easy access
try:
    from .app.main import app as fastapi_app
    from .ui.app import main as streamlit_app
except ImportError:
    # Handle case where dependencies aren't available
    fastapi_app = None
    streamlit_app = None

# Make the package importable
__all__ = ['fastapi_app', 'streamlit_app']
