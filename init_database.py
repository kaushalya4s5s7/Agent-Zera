"""
Database initialization script for Zera Smart Contract Auditing System
Creates the necessary tables for agent memory and learning capabilities
"""

import sqlite3
import asyncio
import aiosqlite
from settings import Settings

async def init_database():
    """Initialize the Zera audit memory database with required tables"""
    settings = Settings()
    
    # Extract database path from connection string
    db_path = settings.memory_connection_string.replace("sqlite+aiosqlite:///", "")
    
    print(f"🔧 Initializing Zera audit database: {db_path}")
    
    async with aiosqlite.connect(db_path) as db:
        # Create conversation_history table for agent interactions
        await db.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                messages_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                agent_name TEXT,
                session_type TEXT DEFAULT 'audit',
                UNIQUE(conversation_id)
            )
        """)
        
        # Create audit_findings table for storing discovered vulnerabilities
        await db.execute("""
            CREATE TABLE IF NOT EXISTS audit_findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_name TEXT NOT NULL,
                contract_hash TEXT,
                vulnerability_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                attack_scenario TEXT,
                remediation TEXT,
                code_snippet TEXT,
                line_numbers TEXT,
                agent_name TEXT DEFAULT 'ZeraSecurityAuditor',
                confidence_score REAL DEFAULT 0.8,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                false_positive BOOLEAN DEFAULT 0
            )
        """)
        
        # Create gas_optimizations table for gas efficiency patterns
        await db.execute("""
            CREATE TABLE IF NOT EXISTS gas_optimizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_name TEXT NOT NULL,
                optimization_type TEXT NOT NULL,
                description TEXT NOT NULL,
                original_code TEXT,
                optimized_code TEXT,
                estimated_gas_savings INTEGER,
                implementation_difficulty TEXT DEFAULT 'medium',
                agent_name TEXT DEFAULT 'GasOptimizer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                verified BOOLEAN DEFAULT 0
            )
        """)
        
        # Create contract_patterns table for recognizing common patterns
        await db.execute("""
            CREATE TABLE IF NOT EXISTS contract_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL,
                pattern_type TEXT NOT NULL, -- 'security_risk', 'gas_inefficient', 'best_practice'
                code_pattern TEXT NOT NULL,
                risk_level TEXT,
                description TEXT,
                examples_count INTEGER DEFAULT 1,
                detection_accuracy REAL DEFAULT 0.8,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(pattern_name, pattern_type)
            )
        """)
        
        # Create audit_sessions table for tracking complete audit runs
        await db.execute("""
            CREATE TABLE IF NOT EXISTS audit_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL UNIQUE,
                contract_name TEXT NOT NULL,
                contract_code_hash TEXT,
                audit_scope TEXT,
                total_vulnerabilities INTEGER DEFAULT 0,
                critical_count INTEGER DEFAULT 0,
                high_count INTEGER DEFAULT 0,
                medium_count INTEGER DEFAULT 0,
                low_count INTEGER DEFAULT 0,
                info_count INTEGER DEFAULT 0,
                gas_optimizations_count INTEGER DEFAULT 0,
                audit_duration_seconds REAL,
                overall_risk_score REAL,
                agents_used TEXT, -- JSON array of agent names
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        
        # Create agent_learning table for storing learning insights
        await db.execute("""
            CREATE TABLE IF NOT EXISTS agent_learning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                learning_type TEXT NOT NULL, -- 'pattern_recognition', 'false_positive', 'accuracy_improvement'
                context TEXT NOT NULL,
                insight TEXT NOT NULL,
                confidence_delta REAL DEFAULT 0.0,
                validation_count INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied_at TIMESTAMP
            )
        """)
        
        # Create indexes for better performance
        await db.execute("CREATE INDEX IF NOT EXISTS idx_conversation_id ON conversation_history(conversation_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_contract_findings ON audit_findings(contract_name, vulnerability_type)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_gas_optimizations ON gas_optimizations(contract_name, optimization_type)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_patterns ON contract_patterns(pattern_type, risk_level)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_sessions ON audit_sessions(session_id, created_at)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_learning ON agent_learning(agent_name, learning_type)")
        
        await db.commit()
        
        print("✅ Database tables created successfully!")
        
        # Insert some initial learning patterns for the agents
        await seed_initial_patterns(db)
        
        print("🧠 Initial learning patterns seeded!")
        print("🔒 Zera audit memory database is ready for agent learning!")

async def seed_initial_patterns(db):
    """Seed the database with initial security patterns and knowledge"""
    
    # Common vulnerability patterns
    initial_patterns = [
        # Reentrancy patterns
        ("Reentrancy Check-Effects-Interactions", "security_risk", 
         "function.*{.*balance.*-=.*external_call.*}", "HIGH",
         "Function modifies state after external call - potential reentrancy"),
        
        # Access control patterns
        ("Missing Access Control", "security_risk",
         "function.*public.*{(?!.*require.*msg\\.sender).*}", "MEDIUM", 
         "Public function without access control checks"),
        
        # tx.origin usage
        ("tx.origin Usage", "security_risk",
         "tx\\.origin\\s*==", "HIGH",
         "Use of tx.origin for authentication is vulnerable to phishing"),
        
        # Gas optimization patterns
        ("Storage to Memory Caching", "gas_inefficient",
         "storage_var\\[.*\\].*storage_var\\[.*\\]", "MEDIUM",
         "Multiple reads from storage should be cached in memory"),
        
        ("Redundant SLOAD", "gas_inefficient", 
         "\\w+\\.\\w+.*\\w+\\.\\w+", "LOW",
         "Multiple reads of same storage variable"),
        
        # Best practices
        ("Custom Errors", "best_practice",
         "require\\(.*,\\s*[\"'].*[\"']\\)", "LOW",
         "Custom errors save gas compared to require strings")
    ]
    
    for pattern_name, pattern_type, code_pattern, risk_level, description in initial_patterns:
        await db.execute("""
            INSERT OR REPLACE INTO contract_patterns 
            (pattern_name, pattern_type, code_pattern, risk_level, description)
            VALUES (?, ?, ?, ?, ?)
        """, (pattern_name, pattern_type, code_pattern, risk_level, description))
    
    await db.commit()

if __name__ == "__main__":
    asyncio.run(init_database())
