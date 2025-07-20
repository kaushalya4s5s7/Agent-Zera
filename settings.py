from pydantic import BaseModel
from typing import Optional
import os

class Settings(BaseModel):
    # API Configuration
    api_key: Optional[str] = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6IjFkY2YyZjI1LTI2MGItNDk3NC1iNmI3LWMzYmUyMzVhZmMwZCIsImV4cCI6NDkwNjQyOTA4MH0.ATps5dX6OhDOHdRW0M1HpH6RBYQ0DGMywXUAiNKN0yg0xvU3meN_TP0sU7WPXiPJh3erGm5ZcsIZY-ND2lP19A"
    base_url: Optional[str] = "https://api.intelligence.io.solutions/api/v1"
    
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