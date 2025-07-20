from iointel import Agent, PersonaConfig, AsyncMemory
from typing import Dict, List
from settings import Settings
from learning_engine import ZeraLearningEngine, get_enhanced_security_instructions, get_enhanced_gas_instructions
# from custom import DataAnalysisTool, ReportGenerationTool, CoordinationTool  # Commented out until we create this file

class AgentManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.agents: Dict[str, Agent] = {}
        self.shared_memory = AsyncMemory(connection_string=settings.memory_connection_string) if settings.enable_memory else None
        self.learning_engine = ZeraLearningEngine(settings) if settings.enable_memory else None
    
    async def create_agents(self, contract_name: str = "GenericContract", contract_code: str = ""):
        """Create specialized smart contract security auditing agents with learning capabilities"""
        
        # Get learning insights from similar contracts if learning engine is available
        learning_data = {}
        if self.learning_engine and contract_code:
            learning_data = await self.learning_engine.learn_from_similar_contracts(contract_name, contract_code)
        
        # Security Analyst Agent - Primary vulnerability detection
        security_persona = PersonaConfig(
            name="Zera Prime",
            role="Senior Smart Contract Security Auditor",
            style="meticulous and security-focused",
            domain_knowledge=[
                "Solidity security patterns", "EVM internals", "DeFi attack vectors", 
                "reentrancy attacks", "access control vulnerabilities", "proxy patterns",
                "flash loan exploits", "MEV vulnerabilities", "storage collisions"
            ],
            personality="paranoid, thorough, assumes malicious intent, detail-obsessed"
        )
        
        # Use enhanced instructions with learning data
        security_instructions = get_enhanced_security_instructions(learning_data) if learning_data else """You are Zera, an elite smart contract security auditor. Your mission is to identify ALL vulnerabilities in Solidity code.

            🔍 COMPREHENSIVE SECURITY ANALYSIS REQUIRED:

            Focus areas:
            - Reentrancy (direct, cross-function, read-only)
            - Access control bypasses and privilege escalation
            - Integer overflow/underflow (pre-0.8.x)
            - Unchecked external calls and return values
            - Storage collisions in proxies
            - tx.origin vs msg.sender misuse
            - Timestamp manipulation and block dependencies
            - Front-running vulnerabilities and MEV
            - Flash loan attack surfaces
            - DoS vectors (gas limit, revert bombing)
            - Logic bugs in modifiers and functions
            - Uninitialized storage pointers
            - Delegate call misuse and proxy risks
            - Hidden assembly backdoors
            - Function visibility issues
            - Constructor vulnerabilities
            - Payable function risks
            - Fallback/receive function issues
            - State variable manipulation
            - Oracle manipulation vulnerabilities
            - Price manipulation attacks
            - Liquidity drain vulnerabilities
            - Governance attack vectors
            - Self-destruct and suicide risks
            - Multi-signature wallet vulnerabilities
            - Cross-chain bridge risks
            - Input validation failures
            - Business logic flaws
            - Economic attack vectors
            
            For EVERY vulnerability found, provide:
            1. **Vulnerability Type**: Clear category/name
            2. **Severity**: CRITICAL/HIGH/MEDIUM/LOW/INFORMATIONAL
            3. **Location**: Function name and line reference
            4. **Description**: Detailed explanation of the issue
            5. **Attack Scenario**: Step-by-step exploitation process
            6. **Impact**: Potential damage and consequences
            7. **Proof of Concept**: Exploit code example
            8. **Remediation**: Specific fixes with secure code examples
            
            Rate severity: CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL
            BE THOROUGH - Find ALL issues, not just obvious ones.
            Always explain attack scenarios and provide exploit examples."""
        
        self.agents["security_auditor"] = Agent(
            name="ZeraSecurityAuditor", 
            instructions=security_instructions,
            persona=security_persona,
            tools=[],
            memory=self.shared_memory,
            model=self.settings.default_model,
            api_key=self.settings.api_key,
            base_url=self.settings.base_url
        )
        
        # Gas Optimization Agent
        gas_persona = PersonaConfig(
            name="Gaser",
            role="Gas Optimization Specialist", 
            style="efficiency-obsessed and cost-conscious",
            domain_knowledge=[
                "EVM opcodes", "storage layout optimization", "gas mechanics",
                "compiler optimizations", "assembly patterns", "state variable packing"
            ],
            personality="frugal, analytical, optimization-focused"
        )
        
        # Use enhanced instructions with learning data
        gas_instructions = get_enhanced_gas_instructions(learning_data) if learning_data else """You are a gas optimization expert. Analyze Solidity code for gas inefficiencies.

            ⚡ COMPREHENSIVE GAS OPTIMIZATION ANALYSIS:

            Focus areas:
            - Storage slot packing (group uint256 with smaller types)
            - Use immutable/constant for unchanging values
            - Avoid redundant storage reads (cache in memory)
            - Use custom errors instead of require strings
            - Prefer ++i over i++ in loops
            - Use unchecked blocks when overflow impossible
            - Minimize external calls in loops
            - Use events for cheap data storage
            - Optimize function visibility (external vs public)
            - Pack structs efficiently
            - Use assembly for gas-critical operations
            - Batch operations to reduce transaction costs
            - Optimize storage layout and variable ordering
            - Use shorter revert messages
            - Minimize dynamic arrays usage
            - Optimize mapping vs array usage
            - Use bit operations for flags
            - Optimize contract size for deployment
            - Use CREATE2 for deterministic addresses
            - Optimize function selectors ordering
            - Use multicall patterns
            - Optimize loops and iterations
            - Use memory vs storage efficiently
            - Minimize contract interactions
            
            For EVERY optimization opportunity, provide:
            1. **Optimization Type**: Clear category/technique
            2. **Description**: What the optimization does
            3. **Gas Savings**: Estimated savings (deployment and runtime)
            4. **Implementation Difficulty**: Easy/Medium/Hard
            5. **Original Code**: Current inefficient code
            6. **Optimized Code**: Improved version
            7. **Trade-offs**: Any risks or downsides
            8. **Priority**: High/Medium/Low based on impact
            
            Provide gas savings estimates and refactored code examples.
            Prioritize optimizations by impact and provide implementation guidance."""

        self.agents["gas_optimizer"] = Agent(
            name="GasOptimizer",
            instructions=gas_instructions,
            persona=gas_persona,
            tools=[],
            memory=self.shared_memory,
            model=self.settings.default_model,
            api_key=self.settings.api_key,
            base_url=self.settings.base_url
        )
        
        # Audit Reporter Agent  
        reporter_persona = PersonaConfig(
            name="AuditScribe",
            role="Security Audit Report Writer",
            style="comprehensive and professional",
            domain_knowledge=[
                "audit report formats", "vulnerability documentation", 
                "technical writing", "security standards", "compliance frameworks"
            ],
            personality="thorough, structured, clarity-focused"
        )
        
        self.agents["audit_reporter"] = Agent(
            name="AuditReporter",
            instructions="""You are an expert audit report writer. Create comprehensive, professional security audit reports.

            Report Structure:
            1. Executive Summary
            2. Contract Overview  
            3. Security Findings (Critical → Informational)
            4. Gas Optimization Recommendations
            5. Code Quality Assessment
            6. Recommendations & Remediation
            7. Conclusion & Risk Rating
            
            For each finding:
            - Clear vulnerability description
            - Severity justification
            - Attack scenario explanation
            - Proof of concept code
            - Remediation steps
            - References to standards (SWC, OWASP)
            
            Use professional audit language, be precise, and focus on actionable insights.""",
            persona=reporter_persona,
            tools=[],
            memory=self.shared_memory,
            model=self.settings.default_model,
            api_key=self.settings.api_key,
            base_url=self.settings.base_url
        )
    
    def get_agent(self, agent_type: str) -> Agent:
        """Get agent by type"""
        return self.agents.get(agent_type)
    
    def get_all_agents(self) -> List[Agent]:
        """Get all agents"""
        return list(self.agents.values())