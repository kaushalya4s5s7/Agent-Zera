"""
Enhanced agent learning module for Zera Smart Contract Auditing System
Provides learning capabilities for agents to improve over time
"""

import asyncio
import aiosqlite
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from settings import Settings

class ZeraLearningEngine:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.db_path = settings.memory_connection_string.replace("sqlite+aiosqlite:///", "")
    
    async def record_audit_session(self, session_data: Dict[str, Any]) -> str:
        """Record a complete audit session for learning"""
        session_id = session_data.get('session_id', self._generate_session_id())
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO audit_sessions 
                (session_id, contract_name, contract_code_hash, audit_scope, 
                 total_vulnerabilities, critical_count, high_count, medium_count, 
                 low_count, info_count, gas_optimizations_count, audit_duration_seconds,
                 overall_risk_score, agents_used, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                session_data.get('contract_name'),
                self._hash_contract(session_data.get('contract_code', '')),
                session_data.get('audit_scope'),
                session_data.get('total_vulnerabilities', 0),
                session_data.get('critical_count', 0),
                session_data.get('high_count', 0),
                session_data.get('medium_count', 0),
                session_data.get('low_count', 0),
                session_data.get('info_count', 0),
                session_data.get('gas_optimizations_count', 0),
                session_data.get('audit_duration_seconds', 0),
                session_data.get('overall_risk_score', 0),
                json.dumps(session_data.get('agents_used', [])),
                datetime.now()
            ))
            await db.commit()
        
        return session_id
    
    async def record_vulnerability_finding(self, finding: Dict[str, Any]):
        """Record a vulnerability finding for pattern learning"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO audit_findings 
                (contract_name, contract_hash, vulnerability_type, severity, 
                 description, attack_scenario, remediation, code_snippet, 
                 line_numbers, agent_name, confidence_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                finding.get('contract_name'),
                finding.get('contract_hash'),
                finding.get('vulnerability_type'),
                finding.get('severity'),
                finding.get('description'),
                finding.get('attack_scenario'),
                finding.get('remediation'),
                finding.get('code_snippet'),
                finding.get('line_numbers'),
                finding.get('agent_name', 'ZeraSecurityAuditor'),
                finding.get('confidence_score', 0.8)
            ))
            await db.commit()
    
    async def record_gas_optimization(self, optimization: Dict[str, Any]):
        """Record a gas optimization for learning"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO gas_optimizations 
                (contract_name, optimization_type, description, original_code, 
                 optimized_code, estimated_gas_savings, implementation_difficulty, agent_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                optimization.get('contract_name'),
                optimization.get('optimization_type'),
                optimization.get('description'),
                optimization.get('original_code'),
                optimization.get('optimized_code'),
                optimization.get('estimated_gas_savings', 0),
                optimization.get('implementation_difficulty', 'medium'),
                optimization.get('agent_name', 'GasOptimizer')
            ))
            await db.commit()
    
    async def learn_from_similar_contracts(self, contract_name: str, contract_code: str) -> Dict[str, Any]:
        """Get learning insights from similar contracts audited before"""
        contract_hash = self._hash_contract(contract_code)
        
        async with aiosqlite.connect(self.db_path) as db:
            # Get similar vulnerabilities found in past audits
            cursor = await db.execute("""
                SELECT vulnerability_type, severity, description, COUNT(*) as frequency
                FROM audit_findings 
                WHERE contract_hash = ? OR contract_name LIKE ?
                GROUP BY vulnerability_type, severity
                ORDER BY frequency DESC, severity
                LIMIT 10
            """, (contract_hash, f"%{contract_name.split('Token')[0] if 'Token' in contract_name else contract_name[:5]}%"))
            
            similar_vulns = await cursor.fetchall()
            
            # Get gas optimization patterns
            cursor = await db.execute("""
                SELECT optimization_type, description, estimated_gas_savings, COUNT(*) as frequency
                FROM gas_optimizations 
                WHERE contract_name LIKE ?
                GROUP BY optimization_type
                ORDER BY frequency DESC, estimated_gas_savings DESC
                LIMIT 5
            """, (f"%{contract_name.split('Token')[0] if 'Token' in contract_name else contract_name[:5]}%",))
            
            gas_patterns = await cursor.fetchall()
            
            # Get pattern recognition insights
            cursor = await db.execute("""
                SELECT pattern_name, pattern_type, risk_level, description, detection_accuracy
                FROM contract_patterns 
                WHERE detection_accuracy > 0.7
                ORDER BY detection_accuracy DESC
            """)
            
            known_patterns = await cursor.fetchall()
        
        return {
            "similar_vulnerabilities": [
                {
                    "type": vuln[0], 
                    "severity": vuln[1], 
                    "description": vuln[2], 
                    "frequency": vuln[3]
                } for vuln in similar_vulns
            ],
            "gas_optimization_patterns": [
                {
                    "type": opt[0], 
                    "description": opt[1], 
                    "avg_savings": opt[2], 
                    "frequency": opt[3]
                } for opt in gas_patterns
            ],
            "known_patterns": [
                {
                    "name": pattern[0], 
                    "type": pattern[1], 
                    "risk": pattern[2], 
                    "description": pattern[3], 
                    "accuracy": pattern[4]
                } for pattern in known_patterns
            ]
        }
    
    async def update_pattern_accuracy(self, pattern_name: str, was_correct: bool):
        """Update pattern detection accuracy based on validation"""
        async with aiosqlite.connect(self.db_path) as db:
            if was_correct:
                await db.execute("""
                    UPDATE contract_patterns 
                    SET detection_accuracy = detection_accuracy * 0.95 + 0.05,
                        examples_count = examples_count + 1,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE pattern_name = ?
                """, (pattern_name,))
            else:
                await db.execute("""
                    UPDATE contract_patterns 
                    SET detection_accuracy = detection_accuracy * 0.95,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE pattern_name = ?
                """, (pattern_name,))
            await db.commit()
    
    async def get_audit_statistics(self) -> Dict[str, Any]:
        """Get overall audit statistics for learning insights"""
        async with aiosqlite.connect(self.db_path) as db:
            # Total audits performed
            cursor = await db.execute("SELECT COUNT(*) FROM audit_sessions")
            total_audits = (await cursor.fetchone())[0]
            
            # Most common vulnerabilities
            cursor = await db.execute("""
                SELECT vulnerability_type, COUNT(*) as count, AVG(confidence_score) as avg_confidence
                FROM audit_findings 
                GROUP BY vulnerability_type 
                ORDER BY count DESC 
                LIMIT 5
            """)
            common_vulns = await cursor.fetchall()
            
            # Average risk scores
            cursor = await db.execute("""
                SELECT AVG(overall_risk_score) as avg_risk,
                       AVG(total_vulnerabilities) as avg_vulns,
                       AVG(gas_optimizations_count) as avg_optimizations
                FROM audit_sessions
                WHERE overall_risk_score IS NOT NULL
            """)
            avg_stats = await cursor.fetchone()
            
            return {
                "total_audits_performed": total_audits,
                "most_common_vulnerabilities": [
                    {"type": v[0], "count": v[1], "avg_confidence": v[2]} 
                    for v in common_vulns
                ],
                "average_risk_score": avg_stats[0] if avg_stats[0] else 0,
                "average_vulnerabilities_per_audit": avg_stats[1] if avg_stats[1] else 0,
                "average_optimizations_per_audit": avg_stats[2] if avg_stats[2] else 0
            }
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"zera_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(datetime.now()) % 10000}"
    
    def _hash_contract(self, contract_code: str) -> str:
        """Generate hash for contract code"""
        return hashlib.md5(contract_code.encode()).hexdigest()

# Enhanced agent instructions with learning capabilities
def get_enhanced_security_instructions(learning_data: Dict[str, Any]) -> str:
    """Generate enhanced security instructions based on learning data"""
    base_instructions = """You are Zera, an elite smart contract security auditor. Your mission is to identify ALL vulnerabilities in Solidity code.

    Focus areas:
    - Reentrancy (direct, cross-function, read-only)
    - Access control bypasses
    - Integer overflow/underflow (pre-0.8.x)
    - Unchecked external calls
    - Storage collisions in proxies
    - tx.origin vs msg.sender misuse
    - Timestamp manipulation
    - Front-running vulnerabilities
    - Flash loan attack surfaces
    - DoS vectors (gas limit, revert bombing)
    - Logic bugs in modifiers
    - Uninitialized storage pointers
    - Delegate call misuse
    - Hidden assembly backdoors
    
    Rate severity: CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL
    Always explain attack scenarios and provide exploit examples."""
    
    if not learning_data:
        return base_instructions
    
    enhanced_instructions = base_instructions + "\n\n🧠 LEARNING INSIGHTS:\n"
    
    if learning_data.get('common_vulnerabilities'):
        enhanced_instructions += f"Based on {learning_data.get('similar_contracts_analyzed', 0)} similar contracts analyzed, pay special attention to:\n"
        for vuln in learning_data['common_vulnerabilities'][:5]:  # Top 5
            enhanced_instructions += f"- {vuln}\n"
    
    if learning_data.get('false_positive_patterns'):
        enhanced_instructions += f"\nAvoid these patterns that are often false positives:\n"
        for pattern in learning_data['false_positive_patterns'][:3]:
            enhanced_instructions += f"- {pattern}\n"
    
    return enhanced_instructions

def get_enhanced_gas_instructions(learning_data: Dict[str, Any]) -> str:
    """Generate enhanced gas optimization instructions based on learning data"""
    base_instructions = """You are a gas optimization expert. Analyze Solidity code for gas inefficiencies.

    Focus areas:
    - Storage slot packing (group uint256 with smaller types)
    - Use immutable/constant for unchanging values
    - Avoid redundant storage reads (cache in memory)
    - Use custom errors instead of require strings
    - Prefer ++i over i++ in loops
    - Use unchecked blocks when overflow impossible
    - Minimize external calls in loops
    - Use events for cheap data storage
    - Optimize function visibility
    - Pack structs efficiently
    - Use assembly for gas-critical operations
    
    Provide gas savings estimates and refactored code examples."""
    
    if not learning_data:
        return base_instructions
    
    enhanced_instructions = base_instructions + "\n\n⚡ LEARNING INSIGHTS:\n"
    
    if learning_data.get('gas_optimization_patterns'):
        enhanced_instructions += f"Based on previous optimizations, prioritize these high-impact patterns:\n"
        for pattern in learning_data['gas_optimization_patterns'][:5]:
            enhanced_instructions += f"- {pattern}\n"
    
    if learning_data.get('average_gas_savings'):
        enhanced_instructions += f"\nTarget gas savings: Aim for optimizations that save at least {learning_data['average_gas_savings']} gas units.\n"
    
    return enhanced_instructions
