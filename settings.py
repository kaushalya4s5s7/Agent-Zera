from pydantic import BaseModel
from typing import Optional
import os

# Try to import streamlit to check for secrets
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get secret from Streamlit secrets or environment variables"""
    # First try Streamlit secrets (for local development)
    if STREAMLIT_AVAILABLE:
        try:
            return st.secrets.get(key, os.getenv(key, default))
        except:
            # Fallback to environment variables if secrets not available
            return os.getenv(key, default)
    else:
        # Fallback to environment variables
        return os.getenv(key, default)

class Settings(BaseModel):
    # API Configuration - Use environment variables and Streamlit secrets
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    
    def __init__(self, **data):
        # Get secrets dynamically
        if not data.get('api_key'):
            data['api_key'] = get_secret('API_KEY')
        if not data.get('base_url'):
            data['base_url'] = get_secret('BASE_URL', 'https://api.intelligence.io.solutions/api/v1')
        
        super().__init__(**data)
    
    # Zera Agent Configuration
    default_model: str = "mistralai/Mistral-Large-Instruct-2411"  # Using supported Mistral model
    max_retries: int = 3
    temperature: float = 0.1  # Lower temperature for more precise security analysis
    
    # Smart Contract Audit Configuration
    enable_memory: bool = True
    memory_connection_string: Optional[str] = os.getenv("MEMORY_CONNECTION_STRING", "sqlite+aiosqlite:///zera_audit_memory.db")
    audit_history_limit: int = 50
    
    # Security Audit Settings
    severity_levels: list = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"]
    supported_solidity_versions: list = ["0.8.x", "0.7.x", "0.6.x", "0.5.x", "0.4.x"]
    audit_depth: str = "comprehensive"  # comprehensive, standard, quick
    
    # Gas Analysis Settings
    gas_optimization_threshold: int = 1000  # Minimum gas savings to report
    include_assembly_optimizations: bool = True
    
    # Logging
    log_level: str = "INFO"
    enable_pretty_output: bool = True