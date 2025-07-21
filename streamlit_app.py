"""
🔒 ZERA - Advanced Smart Contract Security Auditing System
Streamlit Web Interface for Interactive Smart Contract Analysis

Features:
- Interactive contract code input
- Real-time security analysis
- Gas optimization recommendations
- Learning from past audits
- Comprehensive audit reports
- Agent performance analytics
"""

import streamlit as st
import asyncio
import json
import time
import aiosqlite
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any

# Import our Zera components
from agents_manager import AgentManager
from workflow_orchestrator import WorkflowOrchestrator
from settings import Settings
from learning_engine import ZeraLearningEngine

# Page configuration
st.set_page_config(
    page_title="🔒 ZERA - Smart Contract Security Auditor",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling and contrast
st.markdown("""
<style>
    /* Global text improvements */
    .stApp {
        background-color: #ffffff;
        color: #1a1a1a;
    }
    
    /* Main header with better contrast */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a !important;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        padding: 1rem;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 10px;
        border: 1px solid #d1d5db;
    }
    
    /* Improved agent cards with better contrast */
    .agent-card {
        border: 2px solid #d1d5db;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #1a1a1a !important;
    }
    
    .agent-card strong {
        color: #1e3a8a !important;
        font-weight: 600;
    }
    
    /* Vulnerability cards with high contrast */
    .vulnerability-critical {
        background-color: #fef2f2;
        border-left: 6px solid #dc2626;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        color: #0f172a !important;
        box-shadow: 0 2px 4px rgba(220, 38, 38, 0.1);
        border: 1px solid #fecaca;
    }
    
    .vulnerability-critical h4 {
        color: #b91c1c !important;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .vulnerability-critical p {
        color: #0f172a !important;
        line-height: 1.6;
        margin-bottom: 8px;
    }
    
    .vulnerability-critical strong {
        color: #1e293b !important;
        font-weight: 600;
    }
    
    .vulnerability-high {
        background-color: #fffbeb;
        border-left: 6px solid #f59e0b;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        color: #0f172a !important;
        box-shadow: 0 2px 4px rgba(245, 158, 11, 0.1);
        border: 1px solid #fed7aa;
    }
    
    .vulnerability-high h4 {
        color: #d97706 !important;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .vulnerability-high p {
        color: #0f172a !important;
        line-height: 1.6;
        margin-bottom: 8px;
    }
    
    .vulnerability-high strong {
        color: #1e293b !important;
        font-weight: 600;
    }
    
    .vulnerability-medium {
        background-color: #faf5ff;
        border-left: 6px solid #8b5cf6;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        color: #0f172a !important;
        box-shadow: 0 2px 4px rgba(139, 92, 246, 0.1);
        border: 1px solid #ddd6fe;
    }
    
    .vulnerability-medium h4 {
        color: #7c3aed !important;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .vulnerability-medium p {
        color: #0f172a !important;
        line-height: 1.6;
        margin-bottom: 8px;
    }
    
    .vulnerability-medium strong {
        color: #1e293b !important;
        font-weight: 600;
    }
    
    .vulnerability-low {
        background-color: #f0f9ff;
        border-left: 6px solid #3b82f6;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        color: #0f172a !important;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
        border: 1px solid #bfdbfe;
    }
    
    .vulnerability-low h4 {
        color: #2563eb !important;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .vulnerability-low p {
        color: #0f172a !important;
        line-height: 1.6;
        margin-bottom: 8px;
    }
    
    .vulnerability-low strong {
        color: #1e293b !important;
        font-weight: 600;
    }
    
    /* Gas optimization cards */
    .gas-optimization {
        background-color: #f8fafc;
        border-left: 6px solid #10b981;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        color: #0f172a !important;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    .gas-optimization h4 {
        color: #059669 !important;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .gas-optimization p {
        color: #0f172a !important;
        line-height: 1.6;
        margin-bottom: 8px;
    }
    
    .gas-optimization strong {
        color: #1e293b !important;
        font-weight: 600;
    }
    
    /* Enhanced stats cards */
    .stats-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white !important;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: none;
    }
    
    .stats-card h3 {
        color: white !important;
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .stats-card p {
        color: white !important;
        font-weight: 500;
        margin: 0;
    }
    
    /* Improved text readability for all elements */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #1a1a1a !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
    }
    
    .stMarkdown strong {
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }
    
    /* Ensure all text in main content area is visible */
    .main .block-container {
        color: #1a1a1a !important;
    }
    
    /* Fix for any remaining text visibility issues */
    .stApp, .stApp > div, .stApp p, .stApp span {
        color: #1a1a1a !important;
    }
    
    /* Specific fix for info messages */
    .stAlert, .stAlert > div, .stAlert p {
        color: #1e293b !important;
        font-weight: 500 !important;
    }
    
    /* Code blocks with better contrast */
    code {
        background-color: #f1f5f9 !important;
        color: #1e293b !important;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        border: 1px solid #e2e8f0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Metric styling */
    .css-1xarl3l {
        color: #1a1a1a !important;
    }
    
    /* Info boxes with enhanced visibility */
    .stInfo {
        background-color: #f0f9ff !important;
        color: #1e293b !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stInfo > div {
        color: #1e293b !important;
        font-weight: 500 !important;
    }
    
    .stInfo p {
        color: #1e293b !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    
    .stSuccess {
        background-color: #f0fdf4 !important;
        color: #1e293b !important;
        border-left: 4px solid #10b981 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stSuccess > div {
        color: #1e293b !important;
        font-weight: 500 !important;
    }
    
    .stSuccess p {
        color: #1e293b !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    
    .stError {
        background-color: #fef2f2 !important;
        color: #1e293b !important;
        border-left: 4px solid #dc2626 !important;
        border: 1px solid #fecaca !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stError > div {
        color: #1e293b !important;
        font-weight: 500 !important;
    }
    
    .stError p {
        color: #1e293b !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    
    .stWarning {
        background-color: #fffbeb !important;
        color: #1e293b !important;
        border-left: 4px solid #f59e0b !important;
        border: 1px solid #fed7aa !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stWarning > div {
        color: #1e293b !important;
        font-weight: 500 !important;
    }
    
    .stWarning p {
        color: #1e293b !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1e3a8a !important;
        font-weight: 600;
    }
    
    /* Tables */
    .stDataFrame {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }
    
    /* Selectbox and inputs with enhanced contrast */
    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #1e3a8a !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* Selectbox main container */
    .stSelectbox {
        font-size: 16px !important;
    }
    
    /* Selectbox dropdown styling for better contrast */
    .stSelectbox > div > div,
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #374151 !important;
        border-radius: 8px !important;
        min-height: 44px !important;
    }
    
    /* Selectbox dropdown text */
    .stSelectbox > div > div > div,
    .stSelectbox [data-baseweb="select"] > div > div {
        color: #1e293b !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        background-color: #ffffff !important;
    }
    
    /* Selectbox dropdown arrow and button */
    .stSelectbox > div > div button,
    .stSelectbox [data-baseweb="select"] button {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: none !important;
    }
    
    /* Selectbox value display */
    .stSelectbox [data-baseweb="select"] [data-baseweb="tag"] {
        background-color: #ffffff !important;
        color: #1e293b !important;
        font-weight: 500 !important;
        font-size: 16px !important;
    }
    
    /* Selectbox dropdown options container */
    .stSelectbox > div > div > div[role="listbox"],
    .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 2px solid #374151 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        max-height: 300px !important;
        overflow-y: auto !important;
    }
    
    /* Individual selectbox options */
    .stSelectbox > div > div > div[role="listbox"] > div,
    .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] [role="option"] {
        background-color: #ffffff !important;
        color: #1e293b !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        padding: 12px 16px !important;
        border-bottom: 1px solid #e5e7eb !important;
        min-height: 44px !important;
        cursor: pointer !important;
    }
    
    /* Selectbox option hover state */
    .stSelectbox > div > div > div[role="listbox"] > div:hover,
    .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] [role="option"]:hover {
        background-color: #f3f4f6 !important;
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }
    
    /* Selected option in selectbox */
    .stSelectbox > div > div > div[role="listbox"] > div[aria-selected="true"],
    .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] [role="option"][aria-selected="true"] {
        background-color: #dbeafe !important;
        color: #1e3a8a !important;
        font-weight: 700 !important;
    }
    
    /* Selectbox focus state */
    .stSelectbox > div > div:focus-within,
    .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        outline: none !important;
    }
    
    /* Selectbox when open */
    .stSelectbox [data-baseweb="select"][aria-expanded="true"] {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Accessibility improvements for selectbox */
    .stSelectbox * {
        transition: all 0.2s ease !important;
    }
    
    /* High contrast mode for selectbox */
    @media (prefers-contrast: high) {
        .stSelectbox > div > div,
        .stSelectbox [data-baseweb="select"] > div {
            border: 3px solid #000000 !important;
        }
        
        .stSelectbox > div > div > div,
        .stSelectbox [data-baseweb="select"] > div > div {
            color: #000000 !important;
            font-weight: 700 !important;
        }
        
        .stSelectbox > div > div > div[role="listbox"] > div,
        .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] [role="option"] {
            color: #000000 !important;
            border-bottom: 2px solid #000000 !important;
        }
    }
    
    /* Sidebar selectbox specific styling */
    .css-1d391kg .stSelectbox,
    [data-testid="stSidebar"] .stSelectbox {
        margin-bottom: 20px !important;
    }
    
    .css-1d391kg .stSelectbox > div > div,
    [data-testid="stSidebar"] .stSelectbox > div > div,
    .css-1d391kg .stSelectbox [data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #374151 !important;
        border-radius: 8px !important;
        min-height: 44px !important;
        font-size: 16px !important;
    }
    
    .css-1d391kg .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox label {
        color: #1e3a8a !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
    }
    
    /* Sidebar selectbox options container */
    .css-1d391kg .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"],
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 2px solid #374151 !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
        z-index: 9999 !important;
    }
    
    /* Sidebar selectbox individual options */
    .css-1d391kg .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] [role="option"],
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] [role="option"] {
        background-color: #ffffff !important;
        color: #1e293b !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        padding: 12px 16px !important;
        border-bottom: 1px solid #e5e7eb !important;
        min-height: 44px !important;
    }
    
    /* Sidebar selectbox option hover state */
    .css-1d391kg .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] [role="option"]:hover,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] [role="option"]:hover {
        background-color: #f3f4f6 !important;
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar selectbox selected option */
    .css-1d391kg .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] [role="option"][aria-selected="true"],
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] [role="option"][aria-selected="true"] {
        background-color: #dbeafe !important;
        color: #1e3a8a !important;
        font-weight: 700 !important;
    }
    
    /* Enhanced visibility for all alert types including info messages */
    .stAlert[data-baseweb="notification"] {
        background-color: #f0f9ff !important;
        color: #1e293b !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Force high contrast for all text within alerts */
    .stAlert div, .stAlert p, .stAlert span {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Additional rule for info specifically */
    div[data-testid="stAlert"] {
        background-color: #f0f9ff !important;
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Text input styling for high contrast */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        border: 2px solid #374151 !important;
        border-radius: 8px !important;
        color: #1e293b !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        padding: 12px 16px !important;
        min-height: 44px !important;
    }
    
    /* Text input focus state */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        outline: none !important;
    }
    
    /* Button styling for high contrast */
    .stButton > button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 12px 24px !important;
        min-height: 44px !important;
        transition: all 0.2s ease !important;
    }
    
    /* Button hover state */
    .stButton > button:hover {
        background-color: #1e3a8a !important;
        border-color: #1e3a8a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.3) !important;
    }
    
    /* Primary button */
    .stButton[data-testid="baseButton-primary"] > button {
        background-color: #dc2626 !important;
        border-color: #dc2626 !important;
    }
    
    .stButton[data-testid="baseButton-primary"] > button:hover {
        background-color: #991b1b !important;
        border-color: #991b1b !important;
    }
    
    /* Secondary button */
    .stButton[data-testid="baseButton-secondary"] > button {
        background-color: #ffffff !important;
        color: #374151 !important;
        border-color: #374151 !important;
    }
    
    .stButton[data-testid="baseButton-secondary"] > button:hover {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
        border-color: #1f2937 !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border: 2px dashed #374151 !important;
        border-radius: 8px !important;
        background-color: #f9fafb !important;
        padding: 20px !important;
    }
    
    .stFileUploader label {
        color: #1e3a8a !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* Tab styling for high contrast */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f3f4f6 !important;
        color: #374151 !important;
        border: 2px solid #d1d5db !important;
        border-radius: 8px 8px 0 0 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 12px 20px !important;
        min-height: 44px !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border-color: #3b82f6 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e5e7eb !important;
        color: #1f2937 !important;
    }
    
    /* Tab panels */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #ffffff !important;
        border: 2px solid #3b82f6 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 20px !important;
    }
    
    div[data-testid="stAlert"] > div {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Global text visibility override */
    * {
        color: #1e293b !important;
    }
    
    /* Specific override for streamlit alert text */
    .element-container .stAlert .stMarkdown p {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'audit_results' not in st.session_state:
    st.session_state.audit_results = None
if 'audit_history' not in st.session_state:
    st.session_state.audit_history = []
if 'learning_insights' not in st.session_state:
    st.session_state.learning_insights = {}

# Add session reset functionality in sidebar for troubleshooting
with st.sidebar:
    st.markdown("---")
    if st.button("🔄 Reset Session Data", help="Clear all cached audit results and history"):
        st.session_state.audit_results = None
        st.session_state.audit_history = []
        st.session_state.learning_insights = {}
        if 'zera_system' in st.session_state:
            del st.session_state.zera_system
        st.success("Session data cleared!")
        st.rerun()

def initialize_zera_system():
    """Initialize the Zera AI system with validation"""
    if 'zera_system' not in st.session_state:
        try:
            settings = Settings()
            
            # Validate API key
            if not settings.api_key:
                raise ValueError("API key not found. Please set API_KEY in Streamlit secrets or environment variables.")
            
            # Try to initialize components
            agent_manager = AgentManager(settings)
            workflow_orchestrator = WorkflowOrchestrator(agent_manager, settings)
            learning_engine = ZeraLearningEngine(settings)
            
            st.session_state.zera_system = {
                'settings': settings,
                'agent_manager': agent_manager,
                'workflow_orchestrator': workflow_orchestrator,
                'learning_engine': learning_engine
            }
            
        except Exception as e:
            st.error(f"Failed to initialize ZERA system: {str(e)}")
            
            # Show setup instructions
            st.markdown("### 🔧 Setup Instructions for Streamlit Cloud:")
            st.markdown("1. Go to your app settings")
            st.markdown("2. Click on 'Secrets'")
            st.markdown("3. Add your API key:")
            st.code('API_KEY = "your-api-key-here"')
            st.markdown("4. Save and redeploy")
            
            # Return None to indicate failure
            return None
            
    return st.session_state.zera_system

async def run_audit(contract_code: str, contract_name: str, audit_scope: str):
    """Run the complete audit process with error handling"""
    zera_system = initialize_zera_system()
    
    # Check if initialization was successful
    if zera_system is None:
        raise ValueError("ZERA system not properly initialized. Check API configuration.")
    
    # Create agents with contract context
    await zera_system['agent_manager'].create_agents(contract_name, contract_code)
    
    # Run the audit workflow
    results = await zera_system['workflow_orchestrator'].run_full_audit(
        contract_code=contract_code,
        contract_name=contract_name,
        audit_scope=audit_scope
    )
    
    return results

def create_demo_results(contract_code: str, contract_name: str) -> Dict[str, Any]:
    """Create demo results when API is not available - for demonstration purposes"""
    import time
    
    # Simulate audit time
    time.sleep(2)
    
    # Mock results based on contract analysis
    demo_results = {
        "security_findings": [
            {
                "vulnerability_type": "Reentrancy Vulnerability",
                "severity": "CRITICAL",
                "description": "The contract contains a potential reentrancy vulnerability in withdrawal functions.",
                "attack_scenario": "An attacker could exploit this by creating a malicious contract that calls back into the vulnerable function before the state is updated.",
                "remediation": "Use the Checks-Effects-Interactions pattern or implement a reentrancy guard.",
                "code_snippet": "function withdraw() public { /* vulnerable code */ }"
            },
            {
                "vulnerability_type": "Access Control Issue",
                "severity": "HIGH", 
                "description": "Using tx.origin for authorization can be bypassed through contract intermediaries.",
                "attack_scenario": "An attacker can trick a legitimate user into calling a malicious contract that then calls the vulnerable function.",
                "remediation": "Use msg.sender instead of tx.origin for access control checks.",
                "code_snippet": "require(tx.origin == owner)"
            }
        ],
        "gas_optimizations": [
            {
                "optimization_type": "Storage Optimization",
                "description": "Pack struct variables to use fewer storage slots and reduce gas costs.",
                "estimated_gas_savings": "2100",
                "implementation_difficulty": "Low",
                "original_code": "uint256 value; bool flag; uint256 timestamp;",
                "optimized_code": "uint256 value; uint256 timestamp; bool flag;"
            }
        ],
        "overall_risk_score": 7.5,
        "audit_duration_seconds": 2.5,
        "learning_insights": {
            "similar_contracts_analyzed": 45,
            "common_vulnerabilities": ["Reentrancy", "Access Control", "Unchecked Calls"],
            "gas_optimization_patterns": ["Storage Packing", "Loop Caching", "Function Visibility"]
        }
    }
    
    return demo_results

def display_audit_results(results: Dict[str, Any]):
    """Display audit results in a structured format"""
    
    st.subheader("🔍 Audit Results")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_vulnerabilities = len(results.get('security_findings', []))
    gas_optimizations = len(results.get('gas_optimizations', []))
    overall_risk = results.get('overall_risk_score', 0)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <h3>{total_vulnerabilities}</h3>
            <p>Vulnerabilities Found</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <h3>{gas_optimizations}</h3>
            <p>Gas Optimizations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <h3>{overall_risk:.1f}/10</h3>
            <p>Risk Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        audit_time = results.get('audit_duration_seconds', 0)
        st.markdown(f"""
        <div class="stats-card">
            <h3>{audit_time:.1f}s</h3>
            <p>Audit Time</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Security Findings
    if results.get('security_findings'):
        st.subheader("🚨 Security Findings")
        
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFORMATIONAL": 0}
        
        for finding in results['security_findings']:
            severity = finding.get('severity', 'LOW').upper()
            severity_counts[severity] += 1
            
            css_class = f"vulnerability-{severity.lower()}"
            
            st.markdown(f"""
            <div class="{css_class}">
                <h4>🔥 {finding.get('vulnerability_type', 'Unknown Vulnerability')} [{severity}]</h4>
                <p><strong>Description:</strong> <span style="color: #0f172a; font-weight: 500;">{finding.get('description', 'No description available')}</span></p>
                <p><strong>Attack Scenario:</strong> <span style="color: #0f172a; font-weight: 500;">{finding.get('attack_scenario', 'No attack scenario provided')}</span></p>
                <p><strong>Remediation:</strong> <span style="color: #0f172a; font-weight: 500;">{finding.get('remediation', 'No remediation provided')}</span></p>
                {f"<p><strong>Code:</strong> <code style='background-color: #f1f5f9; color: #1e293b; padding: 4px 8px; border-radius: 4px; border: 1px solid #cbd5e1;'>{finding.get('code_snippet', '')}</code></p>" if finding.get('code_snippet') else ""}
            </div>
            """, unsafe_allow_html=True)
        
        # Severity distribution chart
        if severity_counts:
            fig = px.bar(
                x=list(severity_counts.keys()),
                y=list(severity_counts.values()),
                title="Vulnerability Distribution by Severity",
                color=list(severity_counts.keys()),
                color_discrete_map={
                    'CRITICAL': '#dc2626',
                    'HIGH': '#f59e0b',
                    'MEDIUM': '#8b5cf6',
                    'LOW': '#3b82f6',
                    'INFORMATIONAL': '#6b7280'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Gas Optimizations
    if results.get('gas_optimizations'):
        st.subheader("⚡ Gas Optimizations")
        
        total_savings = 0
        for optimization in results['gas_optimizations']:
            savings_raw = optimization.get('estimated_gas_savings', '0')
            
            # Convert string to integer safely with enhanced error handling
            try:
                if isinstance(savings_raw, str):
                    # Remove any non-digit characters except for digits
                    savings_str = ''.join(filter(str.isdigit, savings_raw))
                    savings = int(savings_str) if savings_str else 0
                elif isinstance(savings_raw, (int, float)):
                    savings = int(savings_raw)
                elif savings_raw is None:
                    savings = 0
                else:
                    # Handle any other unexpected types
                    savings_str = ''.join(filter(str.isdigit, str(savings_raw)))
                    savings = int(savings_str) if savings_str else 0
            except (ValueError, TypeError) as e:
                # Debug information for troubleshooting
                st.error(f"Error converting gas savings: {savings_raw} (type: {type(savings_raw)}) - {str(e)}")
                savings = 0
            
            total_savings += savings
            
            st.markdown(f"""
            <div class="gas-optimization">
                <h4>⚡ {optimization.get('optimization_type', 'Gas Optimization')}</h4>
                <p><strong>Description:</strong> <span style="color: #0f172a; font-weight: 500;">{optimization.get('description', 'No description available')}</span></p>
                <p><strong>Estimated Gas Savings:</strong> <span style="color: #059669; font-weight: 700; font-size: 1.1em;">{savings:,} gas units</span></p>
                <p><strong>Difficulty:</strong> <span style="color: #0f172a; font-weight: 500;">{optimization.get('implementation_difficulty', 'Medium')}</span></p>
                {f"<p><strong>Original Code:</strong> <code style='background-color: #fef2f2; color: #1e293b; padding: 8px 12px; border-radius: 6px; display: block; margin: 8px 0; border: 1px solid #fecaca; font-family: Consolas, Monaco, monospace;'>{optimization.get('original_code', '')}</code></p>" if optimization.get('original_code') else ""}
                {f"<p><strong>Optimized Code:</strong> <code style='background-color: #f0fdf4; color: #1e293b; padding: 8px 12px; border-radius: 6px; display: block; margin: 8px 0; border: 1px solid #bbf7d0; font-family: Consolas, Monaco, monospace;'>{optimization.get('optimized_code', '')}</code></p>" if optimization.get('optimized_code') else ""}
            </div>
            """, unsafe_allow_html=True)
        
        st.info(f"💰 Total Estimated Gas Savings: {total_savings:,} gas units")
    
    # Agent Learning Insights
    if results.get('learning_insights'):
        st.subheader("🧠 Learning Insights")
        insights = results['learning_insights']
        
        if insights.get('similar_contracts_analyzed'):
            st.markdown(f"<p style='color: #1a1a1a;'><strong style='color: #1e3a8a;'>📊 Similar Contracts Analyzed:</strong> {insights['similar_contracts_analyzed']}</p>", unsafe_allow_html=True)
        
        if insights.get('common_vulnerabilities'):
            st.markdown("<p style='color: #1e3a8a; font-weight: 600;'>🎯 Common Vulnerability Patterns:</p>", unsafe_allow_html=True)
            for vuln in insights['common_vulnerabilities']:
                st.markdown(f"<p style='color: #1a1a1a; margin-left: 20px;'>• {vuln}</p>", unsafe_allow_html=True)
        
        if insights.get('gas_optimization_patterns'):
            st.markdown("<p style='color: #1e3a8a; font-weight: 600;'>⚡ Gas Optimization Patterns:</p>", unsafe_allow_html=True)
            for pattern in insights['gas_optimization_patterns']:
                st.markdown(f"<p style='color: #1a1a1a; margin-left: 20px;'>• {pattern}</p>", unsafe_allow_html=True)


                

def display_audit_history():
    """Display audit history and analytics"""
    st.subheader("📊 Audit History & Analytics")
    
    if not st.session_state.audit_history:
        st.info("No audit history available yet. Run some audits to see analytics!")
        return
    
    # Convert history to DataFrame
    df = pd.DataFrame(st.session_state.audit_history)
    
    # Time series of audits
    if len(df) > 1:
        fig = px.line(
            df, 
            x='timestamp', 
            y='vulnerabilities_found',
            title="Vulnerabilities Found Over Time",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Contract types analysis
    if 'contract_type' in df.columns:
        contract_types = df['contract_type'].value_counts()
        fig = px.pie(
            values=contract_types.values,
            names=contract_types.index,
            title="Audited Contract Types"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent audits table
    st.subheader("Recent Audits")
    display_df = df[['contract_name', 'vulnerabilities_found', 'gas_optimizations', 'risk_score', 'timestamp']].tail(10)
    st.dataframe(display_df, use_container_width=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🔒 ZERA - Smart Contract Security Auditor</h1>', unsafe_allow_html=True)
    st.markdown("### Advanced AI-Powered Smart Contract Analysis with Learning Capabilities")
    
    # System status check
    try:
        settings = Settings()
        if not settings.api_key:
            st.warning("⚠️ **Demo Mode**: API key not configured. The app will run in demonstration mode with sample results.")
            st.info("To enable full functionality, add your API key to Streamlit secrets: `API_KEY = \"your-key\"`")
        else:
            st.success("✅ **API Configured**: Full functionality available")
    except Exception as e:
        st.error(f"⚠️ Configuration issue: {str(e)}")
    
    # Sidebar
    st.sidebar.title("🛠️ Control Panel")
    
    # Navigation
    page = st.sidebar.selectbox(
        "**:white[Navigate to:]**",
        ["🔍 Contract Audit", "📊 Analytics", "🧠 Learning Engine", "⚙️ Settings"]
    )
    
    if page == "🔍 Contract Audit":
        st.header("Smart Contract Security Audit")
        
        # Contract input section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            contract_name = st.text_input(
                "Contract Name",
                value="MyContract",
                help="Enter a descriptive name for your smart contract"
            )
            
            contract_code = st.text_area(
                "Smart Contract Code (Solidity)",
                height=400,
                placeholder="""pragma solidity ^0.8.0;

contract Example {
    mapping(address => uint256) public balances;
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}""",
                help="Paste your Solidity smart contract code here"
            )
        
        with col2:
            audit_scope = st.selectbox(
                "Audit Scope",
                ["comprehensive", "security-focused", "gas-optimization", "quick-scan"],
                help="Choose the depth and focus of the audit"
            )
            
            st.markdown("### 🤖 Agent Status")
            
            # Agent status indicators
            agents = ["🔍 Security Auditor", "⚡ Gas Optimizer", "📝 Report Writer"]
            for agent in agents:
                st.markdown(f"""
                <div class="agent-card">
                    <strong style="color: #1e293b; font-weight: 700;">{agent}</strong><br>
                    <span style="color: #059669; font-weight: 700; font-size: 0.9em;">● Ready</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Learning insights
            if st.session_state.learning_insights:
                st.markdown("### 🧠 Recent Learning")
                insights = st.session_state.learning_insights
                st.write(f"📈 Patterns learned: {insights.get('patterns_count', 0)}")
                st.write(f"🔍 Similar contracts: {insights.get('similar_contracts', 0)}")
        
        # Audit controls
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🚀 Start Audit", type="primary", use_container_width=True):
                if not contract_code.strip():
                    st.error("Please enter smart contract code to audit!")
                else:
                    with st.spinner("🔍 Running comprehensive security audit..."):
                        # Progress bar
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Simulate audit steps
                        steps = [
                            "Initializing agents...",
                            "Analyzing contract structure...", 
                            "Detecting vulnerabilities...",
                            "Optimizing gas usage...",
                            "Learning from patterns...",
                            "Generating report..."
                        ]
                        
                        for i, step in enumerate(steps):
                            status_text.text(step)
                            progress_bar.progress((i + 1) / len(steps))
                            time.sleep(0.5)
                        
                        # Run actual audit
                        try:
                            # First try the real audit
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            results = loop.run_until_complete(
                                run_audit(contract_code, contract_name, audit_scope)
                            )
                            
                            st.session_state.audit_results = results
                            
                            # Add to history
                            audit_record = {
                                'contract_name': contract_name,
                                'vulnerabilities_found': len(results.get('security_findings', [])),
                                'gas_optimizations': len(results.get('gas_optimizations', [])),
                                'risk_score': results.get('overall_risk_score', 0),
                                'timestamp': datetime.now(),
                                'audit_scope': audit_scope
                            }
                            st.session_state.audit_history.append(audit_record)
                            
                            progress_bar.progress(1.0)
                            status_text.text("✅ Audit completed successfully!")
                            st.success("🎉 Audit completed! Check results below.")
                            
                        except Exception as e:
                            # Enhanced error reporting for deployment debugging
                            import traceback
                            error_details = traceback.format_exc()
                            
                            # Try demo mode as fallback
                            st.warning("⚠️ API unavailable - Running in Demo Mode")
                            try:
                                status_text.text("🔄 Switching to demo mode...")
                                results = create_demo_results(contract_code, contract_name)
                                st.session_state.audit_results = results
                                
                                # Add to history
                                audit_record = {
                                    'contract_name': f"{contract_name} (Demo)",
                                    'vulnerabilities_found': len(results.get('security_findings', [])),
                                    'gas_optimizations': len(results.get('gas_optimizations', [])),
                                    'risk_score': results.get('overall_risk_score', 0),
                                    'timestamp': datetime.now(),
                                    'audit_scope': audit_scope
                                }
                                st.session_state.audit_history.append(audit_record)
                                
                                progress_bar.progress(1.0)
                                status_text.text("✅ Demo audit completed!")
                                st.success("🎉 Demo mode completed! This shows sample results for demonstration.")
                                st.info("ℹ️ To enable full functionality, please configure your API key in Streamlit secrets.")
                                
                            except Exception as demo_error:
                                st.error(f"❌ Both API and demo mode failed: {str(demo_error)}")
                                
                            # Original error handling
                            st.error(f"❌ Original error: {str(e)}")
                            
                            # Show more specific error information in development
                            with st.expander("🔍 Error Details (for debugging)"):
                                st.code(error_details)
                                st.markdown("**Common Deployment Issues:**")
                                st.markdown("- Missing API keys in Streamlit secrets")
                                st.markdown("- Network connectivity issues")
                                st.markdown("- Database initialization problems")
                                st.markdown("- Import/dependency errors")
                            
                            # Check if it's an API key issue
                            if "api_key" in str(e).lower() or "unauthorized" in str(e).lower():
                                st.warning("🔑 **API Key Issue Detected**: Please add your API key to Streamlit secrets")
                                st.info("Go to your app settings → Secrets → Add: `API_KEY = \"your-api-key\"`")
                            
                            st.info("💡 Tip: Make sure your contract code is valid Solidity")
        
        with col2:
            if st.button("📋 Sample Contract", use_container_width=True):
                sample_contract = """pragma solidity ^0.8.0;

contract VulnerableToken {
    mapping(address => uint256) public balances;
    address public owner;
    uint256 public totalSupply;
    
    constructor() {
        owner = msg.sender;
        totalSupply = 1000000 * 10**18;
        balances[owner] = totalSupply;
    }
    
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
    
    function withdraw() public {
        uint256 balance = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");
        balances[msg.sender] = 0;
    }
    
    function changeOwner(address newOwner) public {
        require(tx.origin == owner, "Only owner");
        owner = newOwner;
    }
}"""
                st.text_area("Sample Contract", value=sample_contract, height=200, key="sample")
        
        with col3:
            st.markdown("### 📊 Quick Stats")
            if st.session_state.audit_history:
                total_audits = len(st.session_state.audit_history)
                avg_vulns = sum(a['vulnerabilities_found'] for a in st.session_state.audit_history) / total_audits
                st.metric("Total Audits", total_audits)
                st.metric("Avg. Vulnerabilities", f"{avg_vulns:.1f}")
        
        # Display results
        if st.session_state.audit_results:
            st.markdown("---")
            display_audit_results(st.session_state.audit_results)
    
    elif page == "📊 Analytics":
        display_audit_history()
    
    elif page == "🧠 Learning Engine":
        st.header("Agent Learning Engine")
        zera_system = initialize_zera_system()
        learning_engine = zera_system['learning_engine'] if zera_system else None
        # Remove any local import asyncio
        def fetch_learning_stats_sync():
            return asyncio.run(learning_engine.get_audit_statistics()) if learning_engine else None
        def fetch_recent_learnings_sync():
            # Fetch recent learnings directly from the database using the backend
            if learning_engine:
                recent_learnings = asyncio.run(learning_engine.get_recent_learnings())
                recent_vulns = recent_learnings.get('common_vulnerabilities', [])
                recent_gas_patterns = recent_learnings.get('gas_optimization_patterns', [])
                return recent_vulns, recent_gas_patterns
            return [], []
        stats = fetch_learning_stats_sync()
        recent_vulns, recent_gas_patterns = fetch_recent_learnings_sync()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Learning Statistics")
            if stats:
                st.metric("Patterns Learned", stats.get("total_audits_performed", 0))
                st.metric("Avg. Vulnerabilities", f"{stats.get('average_vulnerabilities_per_audit', 0):.1f}")
                st.metric("Avg. Optimizations", f"{stats.get('average_optimizations_per_audit', 0):.1f}")
                st.metric("Avg. Risk Score", f"{stats.get('average_risk_score', 0):.2f}")
            else:
                st.info("No learning statistics available yet.")
        with col2:
            st.subheader("🎯 Recent Learnings")
            if recent_vulns:
                st.markdown("<strong>Common Vulnerabilities:</strong>", unsafe_allow_html=True)
                for learning in recent_vulns:
                    st.markdown(f"<p style='color: #1a1a1a;'>• {learning}</p>", unsafe_allow_html=True)
            if recent_gas_patterns:
                st.markdown("<strong>Gas Optimization Patterns:</strong>", unsafe_allow_html=True)
                for pattern in recent_gas_patterns:
                    st.markdown(f"<p style='color: #1a1a1a;'>• {pattern}</p>", unsafe_allow_html=True)
            if not recent_vulns and not recent_gas_patterns:
                st.info("No recent learnings available yet.")
        st.subheader("🔄 Learning Configuration")
        col1, col2 = st.columns(2)
        with col1:
            learning_rate = st.slider("Learning Rate", 0.1, 1.0, 0.7)
            pattern_threshold = st.slider("Pattern Recognition Threshold", 0.5, 0.95, 0.8)
        with col2:
            enable_auto_learning = st.checkbox("Enable Auto-Learning", True)
            save_patterns = st.checkbox("Save New Patterns", True)
        if st.button("🔄 Retrain Learning Models"):
            with st.spinner("Retraining learning models and refreshing stats..."):
                if learning_engine:
                    # Fetch stats before retraining
                    async def get_pattern_stats():
                        async with aiosqlite.connect(learning_engine.db_path) as db:
                            cursor = await db.execute("SELECT COUNT(*), AVG(detection_accuracy) FROM contract_patterns")
                            count, avg_acc = await cursor.fetchone()
                            return count, avg_acc
                    before_count, before_acc = asyncio.run(get_pattern_stats())
                    # Call backend retrain method with config values
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    retrain_result = loop.run_until_complete(
                        learning_engine.retrain(
                            learning_rate=learning_rate,
                            pattern_threshold=pattern_threshold,
                            enable_auto_learning=enable_auto_learning,
                            save_patterns=save_patterns
                        )
                    )
                    # Fetch stats after retraining
                    after_count, after_acc = asyncio.run(get_pattern_stats())
                    # Show before/after stats
                    st.info(f"Patterns: {before_count} → {after_count}, Avg. Accuracy: {before_acc:.3f} → {after_acc:.3f}")
                    st.info(f"Retrain result: {retrain_result}")
                    # Refresh stats and recent learnings after retraining
                    stats = asyncio.run(learning_engine.get_audit_statistics())
                    recent_vulns, recent_gas_patterns = fetch_recent_learnings_sync()
                st.success("✅ Learning models retrained and stats refreshed!")
    
    elif page == "⚙️ Settings":
        st.header("System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🤖 Agent Settings")
            
            model_selection = st.selectbox(
                "AI Model",
                ["meta-llama/Llama-3.3-70B-Instruct", "gpt-4", "claude-3-sonnet"],
                help="Choose the AI model for analysis"
            )
            
            temperature = st.slider(
                "Analysis Temperature",
                0.0, 1.0, 0.1,
                help="Higher values make analysis more creative, lower values more precise"
            )
            
            max_retries = st.number_input("MaxRetries", 1, 10, 3)
        
        with col2:
            st.subheader("🔧 Audit Settings")
            
            audit_depth = st.selectbox(
                "Default Audit Depth",
                ["comprehensive", "standard", "quick"]
            )
            
            gas_threshold = st.number_input(
                "Gas Optimization Threshold",
                100, 10000, 1000,
                help="Minimum gas savings to report (in gas units)"
            )
            
            enable_assembly = st.checkbox("Include Assembly Optimizations", True)
        
        st.subheader("💾 Database Settings")
        
        db_path = st.text_input(
            "Database Path",
            "sqlite:///zera_audit_memory.db",
            help="Path to the learning database"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 Clear Audit History"):
                st.session_state.audit_history = []
                st.success("Audit history cleared!")
        
        with col2:
            if st.button("💾 Export Settings"):
                settings_json = {
                    "model": model_selection,
                    "temperature": temperature,
                    "max_retries": max_retries,
                    "audit_depth": audit_depth,
                    "gas_threshold": gas_threshold
                }
                st.download_button(
                    "Download Settings",
                    json.dumps(settings_json, indent=2),
                    "zera_settings.json",
                    "application/json"
                )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #1e3a8a; font-weight: 600;'>"
        "🔒 <strong>ZERA AI</strong> - Advanced Smart Contract Security Auditing System | "
        "Built with ❤️ for Web3 Security</p>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
