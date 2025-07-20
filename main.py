"""
🔒 ZERA - Advanced Smart Contract Security Auditing System
An intelligent multi-agent system specialized in Solidity security analysis

Agents:
- ZeraSecurityAuditor: Identifies vulnerabilities and attack vectors
- GasOptimizer: Finds gas efficiency improvements  
- AuditReporter: Generates comprehensive audit reports

Capabilities:
- Comprehensive security vulnerability detection
- Gas optimization analysis
- Professional audit report generation
- Multi-agent collaborative analysis
"""

import asyncio
from agents_manager import AgentManager
from workflow_orchestrator import WorkflowOrchestrator
from settings import Settings
# from tools.custom_tools import DataAnalysisTool, ReportGenerationTool  # Commented out until we create this file

async def main():
    # Initialize settings
    settings = Settings()
    
    # Create agent manager
    agent_manager = AgentManager(settings)
    
    # Smart contract to audit (example)
    sample_contract = """
    pragma solidity ^0.8.0;
    
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
            require(msg.sender == owner, "Only owner");
            payable(owner).call{value: address(this).balance}("");
        }
        
        function mint(address to, uint256 amount) public {
            require(tx.origin == owner, "Only owner");
            balances[to] += amount;
            totalSupply += amount;
        }
    }
    """
    
    # Create specialized agents with contract context
    await agent_manager.create_agents(
        contract_name="VulnerableToken",
        contract_code=sample_contract
    )
    
    # Initialize workflow orchestrator
    orchestrator = WorkflowOrchestrator(agent_manager)
    
    # Run Zera smart contract security audit
    result = await orchestrator.run_security_audit_pipeline(
        contract_code=sample_contract,
        contract_name="VulnerableToken",
        audit_scope="Full security review with gas optimization"
    )
    
    print(f"🔒 Zera Security Audit Completed: {result['status']}")
    print(f"📊 Findings: {len(result.get('security_findings', []))} security issues identified")
    print(f"⛽ Gas Optimizations: {len(result.get('gas_optimizations', []))} improvements found")

if __name__ == "__main__":
    asyncio.run(main())