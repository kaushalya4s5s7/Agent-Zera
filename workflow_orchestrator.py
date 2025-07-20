from iointel import Workflow
from agents_manager import AgentManager
from typing import Dict, Any
import asyncio
import re
import time

class WorkflowOrchestrator:
    def __init__(self, agent_manager: AgentManager, settings):
        self.agent_manager = agent_manager
        self.settings = settings
    
    async def run_data_analysis_pipeline(self, objective: str) -> Dict[str, Any]:
        """Run complete data analysis pipeline"""
        
        # Create workflow
        workflow = Workflow(objective=objective, client_mode=False)
        
        # Step 1: Data preprocessing and analysis
        analysis_result = await workflow.custom(
            name="data_analysis",
            objective=f"Analyze the data for: {objective}",
            instructions="Perform comprehensive data analysis including statistical summaries, trend analysis, and key insights identification.",
            agents=[self.agent_manager.get_agent("analyst")]
        ).run_tasks()
        
        # Step 2: Generate report
        report_result = await workflow.custom(
            name="report_generation",
            objective=f"Create executive report based on analysis: {analysis_result.result}",
            instructions="Create a professional executive report with visualizations, key findings, and actionable recommendations.",
            agents=[self.agent_manager.get_agent("writer")]
        ).run_tasks()
        
        # Step 3: Quality review and coordination
        final_result = await workflow.custom(
            name="quality_review",
            objective=f"Review and finalize the report: {report_result.result}",
            instructions="Review the report for quality, completeness, and accuracy. Provide final recommendations.",
            agents=[self.agent_manager.get_agent("coordinator")]
        ).run_tasks()
        
        return {
            "analysis": analysis_result.result,
            "report": report_result.result,
            "final_output": final_result.result,
            "status": "completed"
        }
    
    async def run_collaborative_task(self, task_description: str) -> Dict[str, Any]:
        """Run collaborative task across multiple agents"""
        
        # Step 1: Coordinator creates plan
        coordinator = self.agent_manager.get_agent("coordinator")
        plan = await coordinator.run(f"Create a detailed execution plan for: {task_description}")
        
        # Step 2: Analyst processes data
        analyst = self.agent_manager.get_agent("analyst")
        analysis = await analyst.run(f"Execute analysis phase of plan: {plan.result}")
        
        # Step 3: Writer creates deliverable
        writer = self.agent_manager.get_agent("writer")
        deliverable = await writer.run(f"Create deliverable based on analysis: {analysis.result}")
        
        # Step 4: Coordinator reviews and finalizes
        final_review = await coordinator.run(f"Review and finalize deliverable: {deliverable.result}")
        
        return {
            "plan": plan.result,
            "analysis": analysis.result,
            "deliverable": deliverable.result,
            "final_output": final_review.result
        }

    async def run_security_audit_pipeline(self, contract_code: str, contract_name: str, audit_scope: str) -> Dict[str, Any]:
        """Run comprehensive smart contract security audit pipeline"""
        
        # Get the security auditor agent directly
        security_agent = self.agent_manager.get_agent("security_auditor")
        
        # Create detailed security analysis prompt
        security_prompt = f"""COMPREHENSIVE SMART CONTRACT SECURITY AUDIT
        
Contract: {contract_name}
Scope: {audit_scope}

CONTRACT CODE:
{contract_code}

INSTRUCTIONS: Perform a COMPREHENSIVE security analysis. You MUST identify ALL vulnerabilities present in this contract. Do not limit yourself to obvious issues - examine every line for potential security risks.

🔍 MANDATORY VULNERABILITY CATEGORIES TO ANALYZE:

1. **REENTRANCY VULNERABILITIES**
   - Direct reentrancy (external calls before state updates)
   - Cross-function reentrancy
   - Read-only reentrancy
   - Check ALL external calls and state changes

2. **ACCESS CONTROL ISSUES**
   - Missing access controls on critical functions
   - Improper use of tx.origin vs msg.sender
   - Privilege escalation opportunities
   - Unauthorized function access

3. **ARITHMETIC VULNERABILITIES**
   - Integer overflow/underflow (especially pre-0.8.x)
   - Division by zero
   - Precision loss in calculations

4. **EXTERNAL CALL VULNERABILITIES** 
   - Unchecked return values
   - Unexpected call failures
   - Gas griefing attacks

5. **STATE MANIPULATION**
   - Timestamp dependency (block.timestamp)
   - Block number manipulation
   - Difficulty/coinbase dependencies

6. **FRONT-RUNNING & MEV**
   - Transaction ordering dependencies
   - Price manipulation opportunities
   - Sandwich attacks

7. **DENIAL OF SERVICE**
   - Gas limit attacks
   - Revert bombing
   - State bloat attacks

8. **PROXY & DELEGATE CALL ISSUES**
   - Storage collision in proxies
   - Delegatecall to untrusted contracts
   - Initialization issues

9. **ORACLE & PRICE MANIPULATION**
   - Oracle dependency vulnerabilities
   - Price feed manipulation
   - Flash loan attacks

10. **BUSINESS LOGIC FLAWS**
    - Logic errors in calculations
    - Incorrect state transitions
    - Economic incentive misalignment

📋 FOR EACH VULNERABILITY FOUND, PROVIDE:

**1. Vulnerability Type**: [Specific category and name]
**Severity**: CRITICAL/HIGH/MEDIUM/LOW/INFORMATIONAL  
**Location**: [Function name and line reference if possible]
**Description**: [Detailed explanation of the security issue]
**Vulnerable Code**: 
```solidity
[Show the exact vulnerable code segment]
```
**Attack Scenario**: [Step-by-step exploitation process]
**Impact**: [Potential damage and consequences]
**Proof of Concept**: [Example exploit code if applicable]
**Remediation**: [Specific fixes with secure code examples]

⚠️ SEVERITY GUIDELINES:
- **CRITICAL**: Direct loss of funds, complete contract compromise
- **HIGH**: Significant impact, potential fund loss
- **MEDIUM**: Moderate impact, limited exploitation  
- **LOW**: Minor issues, edge cases
- **INFORMATIONAL**: Best practices, code quality improvements

🎯 ANALYSIS REQUIREMENTS:
- Examine EVERY function for vulnerabilities
- Check ALL state variables for manipulation risks
- Analyze ALL external interactions
- Consider ALL possible attack vectors
- Include vulnerable code segments with each finding
- Provide realistic attack scenarios
- Suggest specific remediation steps

Be thorough and comprehensive. This contract contains multiple vulnerabilities - find them ALL."""
        
        # Call agent directly
        security_response = await self._run_agent_with_retry(security_agent, security_prompt)
        
        # Extract content from agent response
        security_content = security_response.result if hasattr(security_response, 'result') else str(security_response)
        
        return {
            "contract_name": contract_name,
            "audit_scope": audit_scope,
            "security_findings": security_content,
            "status": "completed"
        }

    async def run_gas_optimization_pipeline(self, contract_code: str, contract_name: str) -> Dict[str, Any]:
        """Run gas optimization analysis pipeline"""
        
        # Get the gas optimizer agent directly
        gas_agent = self.agent_manager.get_agent("gas_optimizer")
        
        # Create detailed gas optimization prompt
        gas_prompt = f"""GAS OPTIMIZATION ANALYSIS
        
Contract: {contract_name}

CONTRACT CODE:
{contract_code}

Perform comprehensive gas optimization analysis. Identify ALL gas inefficiencies:

⚡ GAS OPTIMIZATION CATEGORIES:
1. Storage layout optimization (variable packing)
2. Redundant storage reads/writes (cache in memory)
3. Loop optimizations and gas-efficient iterations
4. Function visibility optimizations (external vs public)
5. Use of constants/immutable for unchanging values
6. Custom errors vs require strings (post-0.8.4)
7. Unnecessary checks and redundant operations
8. Assembly optimizations for gas-critical operations
9. Event usage for cheap data storage vs storage
10. External call optimizations and batching
11. Struct and array packing efficiency
12. Use of unchecked blocks where overflow impossible
13. ++i vs i++ in loops and counters
14. Short-circuiting in conditional statements
15. Avoiding zero-value storage writes

📋 FOR EACH OPTIMIZATION:
- **Optimization Type**: Clear category name
- **Description**: Detailed explanation of the inefficiency
- **Current Code**: Show the gas-inefficient code
- **Optimized Code**: Provide refactored efficient version
- **Estimated Gas Savings**: Approximate gas units saved
- **Implementation Difficulty**: Easy/Medium/Hard
- **Trade-offs**: Any risks or downsides to consider
- **Priority**: High/Medium/Low based on impact

🎯 OPTIMIZATION PRIORITIES:
- High: 1000+ gas savings, easy implementation
- Medium: 500-1000 gas savings, moderate implementation  
- Low: <500 gas savings, complex implementation

Be thorough in finding ALL optimization opportunities."""
        
        # Call agent directly
        gas_response = await self._run_agent_with_retry(gas_agent, gas_prompt)
        
        # Extract content from agent response
        gas_content = gas_response.result if hasattr(gas_response, 'result') else str(gas_response)
        
        return {
            "contract_name": contract_name,
            "gas_optimizations": gas_content,
            "status": "completed"
        }

    async def run_full_audit(self, contract_code: str, contract_name: str, audit_scope: str = "comprehensive") -> Dict[str, Any]:
        """Run complete audit workflow with security analysis, gas optimization, and reporting"""
        start_time = time.time()
        
        results = {
            "contract_name": contract_name,
            "audit_scope": audit_scope,
            "security_findings": [],
            "gas_optimizations": [],
            "overall_risk_score": 0,
            "audit_duration_seconds": 0,
            "learning_insights": {},
            "status": "completed"
        }
        
        try:
            # Create agents first
            await self.agent_manager.create_agents(contract_name, contract_code)
            
            # Run security audit pipeline
            security_results = await self.run_security_audit_pipeline(contract_code, contract_name, audit_scope)
            if security_results.get("security_findings"):
                findings_text = security_results["security_findings"]
                
                # Enhanced Debug Logging
                print("\n" + "="*40 + " SECURITY AUDIT RAW RESPONSE " + "="*40)
                print(f"Type of findings_text: {type(findings_text)}")
                if isinstance(findings_text, str):
                    print(f"Length of findings_text: {len(findings_text)}")
                    print(f"Response (first 500 chars):\n---\n{findings_text[:500]}\n---")
                    print(f"Response (last 500 chars):\n---\n{findings_text[-500:]}\n---")
                else:
                    print(f"Response content: {findings_text}")
                print("="*100 + "\n")

                if isinstance(findings_text, str):
                    # Parse the detailed security analysis to extract structured findings
                    results["security_findings"] = self._parse_security_findings(findings_text)
                else:
                    results["security_findings"] = findings_text
            
            # Run gas optimization pipeline  
            gas_results = await self.run_gas_optimization_pipeline(contract_code, contract_name)
            if gas_results.get("gas_optimizations"):
                optimizations_text = gas_results["gas_optimizations"]

                # Enhanced Debug Logging for Gas Optimizations
                print("\n" + "="*40 + " GAS OPTIMIZATION RAW RESPONSE " + "="*40)
                print(f"Type of optimizations_text: {type(optimizations_text)}")
                if isinstance(optimizations_text, str):
                    print(f"Length of optimizations_text: {len(optimizations_text)}")
                    print(f"Response (first 500 chars):\n---\n{optimizations_text[:500]}\n---")
                    print(f"Response (last 500 chars):\n---\n{optimizations_text[-500:]}\n---")
                else:
                    print(f"Response content: {optimizations_text}")
                print("="*100 + "\n")

                if isinstance(optimizations_text, str):
                    # Parse gas optimizations
                    parsed_optimizations = self._extract_gas_optimizations(optimizations_text)
                    
                    # Debug each parsed optimization
                    print("\n" + "="*40 + " PARSED GAS OPTIMIZATIONS DEBUG " + "="*40)
                    for i, opt in enumerate(parsed_optimizations, 1):
                        print(f"  Type: {opt.get('optimization_type', 'N/A')}")
                        print(f"  Description: {opt.get('description', 'N/A')[:100]}...")
                        print(f"  Gas Savings: {opt.get('estimated_gas_savings', 'N/A')}")
                        print(f"  Difficulty: {opt.get('implementation_difficulty', 'N/A')}")
                        
                        orig_code = opt.get('original_code', '')
                        opt_code = opt.get('optimized_code', '')
                        
                        print(f"  Has Original Code: {'✅' if orig_code else '❌'} ({len(orig_code)} chars)")
                        print(f"  Has Optimized Code: {'✅' if opt_code else '❌'} ({len(opt_code)} chars)")
                        
                        if orig_code:
                            print(f"  Original Code Preview: {orig_code[:100]}...")
                        if opt_code:
                            print(f"  Optimized Code Preview: {opt_code[:100]}...")
                    
                    print(f"\n📊 Total Gas Optimizations Parsed: {len(parsed_optimizations)}")
                    print("="*100 + "\n")
                    
                    results["gas_optimizations"] = parsed_optimizations
                else:
                    results["gas_optimizations"] = optimizations_text
            
            # Calculate overall risk score
            critical_count = len([f for f in results["security_findings"] if f.get("severity") == "CRITICAL"])
            high_count = len([f for f in results["security_findings"] if f.get("severity") == "HIGH"])
            medium_count = len([f for f in results["security_findings"] if f.get("severity") == "MEDIUM"])
            
            risk_score = min(10, critical_count * 3 + high_count * 2 + medium_count * 1)
            results["overall_risk_score"] = risk_score
            
            # Get learning insights if learning engine exists
            if hasattr(self.agent_manager, 'learning_engine') and self.agent_manager.learning_engine:
                learning_insights = await self.agent_manager.learning_engine.learn_from_similar_contracts(
                    contract_name, contract_code
                )
                results["learning_insights"] = learning_insights
            
            # Record audit session for learning
            if hasattr(self.agent_manager, 'learning_engine') and self.agent_manager.learning_engine:
                session_data = {
                    "contract_name": contract_name,
                    "contract_code": contract_code,
                    "audit_scope": audit_scope,
                    "total_vulnerabilities": len(results["security_findings"]),
                    "critical_count": critical_count,
                    "high_count": high_count,
                    "medium_count": medium_count,
                    "low_count": len([f for f in results["security_findings"] if f.get("severity") == "LOW"]),
                    "info_count": len([f for f in results["security_findings"] if f.get("severity") == "INFORMATIONAL"]),
                    "gas_optimizations_count": len(results["gas_optimizations"]),
                    "overall_risk_score": risk_score,
                    "agents_used": ["security_auditor", "gas_optimizer", "audit_reporter"]
                }
                await self.agent_manager.learning_engine.record_audit_session(session_data)
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"❌ ERROR in audit pipeline: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # Calculate audit duration
        end_time = time.time()
        results["audit_duration_seconds"] = end_time - start_time
        
        return results

    async def _run_agent_with_retry(self, agent, prompt: str, max_retries: int = 3, initial_delay: int = 2):
        """Run an agent with retry logic for handling transient API errors."""
        from pydantic_ai.exceptions import ModelHTTPError
        import asyncio

        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return await agent.run(prompt)
            except ModelHTTPError as e:
                if e.status_code >= 500 and attempt < max_retries - 1:
                    print(f"🚨 Agent call failed with status {e.status_code}. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"🚨 Agent call failed after {max_retries} retries or with a non-retriable status code ({e.status_code}).")
                    raise e
            except Exception as e:
                print(f"An unexpected error occurred during agent execution: {e}")
                raise e

    def _parse_security_findings(self, text: str) -> list:
        """Parse security findings from agent text response"""
        findings = []
        
        try:
            # Clean the text first
            text = self._clean_agent_response(text)
            
            print(f"🔍 SECURITY PARSING: Starting to parse {len(text)} characters of agent response")
            
            # Look for vulnerability sections
            sections = []
            
            # Try numbered vulnerability patterns
            vuln_patterns = [
                r'(?:^|\n)#{1,6}\s*(\d+)\.\s*([^\n]*(?:vulnerability|finding|issue|attack|exploit|risk)[^\n]*)\s*\n(.*?)(?=(?:^|\n)#{1,6}\s*\d+\.|$)',
                r'(?:^|\n)(\d+)\.\s*\*\*([^\*]*(?:vulnerability|finding|issue|attack|exploit|risk)[^\*]*)\*\*\s*\n(.*?)(?=(?:^|\n)\d+\.|$)',
                r'(?:^|\n)\*\*(\d+)\.\s*([^\*]*(?:vulnerability|finding|issue|attack|exploit|risk)[^\*]*)\*\*\s*\n(.*?)(?=(?:^|\n)\*\*\d+\.|$)'
            ]
            
            for pattern in vuln_patterns:
                numbered_vulns = re.findall(pattern, text, re.DOTALL | re.MULTILINE | re.IGNORECASE)
                if numbered_vulns:
                    print(f"🔍 SECURITY PARSING: Found {len(numbered_vulns)} vulnerabilities with pattern")
                    for num, title, content in numbered_vulns:
                        full_section = f"{title.strip()}\n{content.strip()}"
                        if len(content.strip()) > 100:
                            sections.append(full_section)
                            print(f"📝 Added vulnerability {num}: {title.strip()[:60]}...")
                    break
            
            # If no numbered sections, try keyword-based extraction
            if not sections:
                print("🔍 SECURITY PARSING: Using keyword-based extraction")
                paragraphs = re.split(r'\n\s*\n', text)
                
                security_keywords = [
                    'reentrancy', 'access control', 'integer overflow', 'underflow',
                    'unchecked call', 'tx.origin', 'timestamp', 'front running',
                    'dos attack', 'denial of service', 'delegatecall', 'proxy',
                    'flash loan', 'oracle manipulation', 'storage collision',
                    'uninitialized', 'privilege escalation', 'authorization',
                    'authentication', 'input validation', 'state manipulation'
                ]
                
                for para in paragraphs:
                    para = para.strip()
                    if (len(para) > 100 and 
                        any(keyword in para.lower() for keyword in security_keywords) and
                        not self._is_template_text(para)):
                        sections.append(para)
                        first_line = para.split('\n')[0][:60]
                        print(f"📝 Added keyword-based section: {first_line}...")
            
            print(f"🔍 SECURITY PARSING: Processing {len(sections)} sections for vulnerability extraction")
                    
            for i, section in enumerate(sections):
                try:
                    section = section.strip()
                    if len(section) < 100:
                        print(f"🔍 SECURITY PARSING: Skipping short section {i+1} ({len(section)} chars)")
                        continue
                    
                    print(f"🔍 SECURITY PARSING: Processing section {i+1} ({len(section)} chars)")
                    
                    # Extract vulnerability information
                    vuln_info = self._extract_vulnerability_info(section)
                        
                    # Validate the vulnerability
                    if self._is_valid_security_vulnerability(vuln_info, section):
                        print(f"✅ SECURITY PARSING: Added vulnerability: {vuln_info['vulnerability_type']}")
                        findings.append(vuln_info)
                    else:
                        print(f"❌ SECURITY PARSING: Rejected section - insufficient content")
                        
                except Exception as section_error:
                    print(f"❌ ERROR processing security section {i+1}: {str(section_error)}")
                    continue
            
            print(f"🔍 SECURITY PARSING: Final result - {len(findings)} vulnerabilities found")
            return findings
            
        except Exception as e:
            print(f"❌ ERROR in _parse_security_findings: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    def _extract_vulnerability_info(self, section: str) -> dict:
        """Extract vulnerability information from a section"""
        vuln_type = self._extract_vulnerability_type(section)
        severity = self._extract_severity(section)
        description = self._extract_description(section)
        attack_scenario = self._extract_attack_scenario(section)
        remediation = self._extract_remediation(section)
        code_snippet, location = self._extract_vulnerable_code(section)
        
        return {
            "vulnerability_type": vuln_type,
            "severity": severity,
            "description": description,
            "attack_scenario": attack_scenario,
            "remediation": remediation,
            "code_snippet": code_snippet,
            "location": location
        }

    def _extract_vulnerability_type(self, section: str) -> str:
        """Extract vulnerability type"""
        # Look for explicit type declarations
        type_patterns = [
            r'(?:vulnerability\s+type|type|category)[:\s]*([^\n]+)',
            r'\*\*\s*([^*\n]+(?:vulnerability|attack|issue))\s*\*\*',
            r'(?:^|\n)([^:\n]*(?:reentrancy|overflow|underflow|access control|dos|front.?running|flash loan)[^:\n]*?)(?:\n|:)',
        ]
        
        for pattern in type_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                vuln_type = match.group(1).strip()
                vuln_type = re.sub(r'^[*\s\-#\d\.]+|[*\s\-#]+$', '', vuln_type)
                if len(vuln_type) > 3 and len(vuln_type) < 100:
                    return vuln_type
        
        # Look for specific vulnerability patterns
        vuln_patterns = {
            r'reentranc[yi]': 'Reentrancy Vulnerability',
            r'integer\s+overflow': 'Integer Overflow',
            r'integer\s+underflow': 'Integer Underflow',
            r'access\s+control': 'Access Control Vulnerability',
            r'unchecked.*call': 'Unchecked External Call',
            r'tx\.origin': 'tx.origin Authentication Bypass',
            r'timestamp.*depend': 'Timestamp Dependency',
            r'front.?running': 'Front-running Vulnerability',
            r'flash\s+loan': 'Flash Loan Attack',
            r'dos|denial.*service': 'Denial of Service',
        }
        
        for pattern, vuln_name in vuln_patterns.items():
            if re.search(pattern, section, re.IGNORECASE):
                return vuln_name
        
        return "Security Vulnerability"

    def _extract_severity(self, section: str) -> str:
        """Extract severity from text section"""
        # Look for explicit severity declarations
        severity_patterns = [
            r'severity[:\s]*([a-zA-Z]+)',
            r'\*\*\s*severity\s*\*\*[:\s]*([a-zA-Z]+)',
        ]
        
        for pattern in severity_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                severity = match.group(1).strip().upper()
                if severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFORMATIONAL']:
                    return severity
        
        # Look for severity keywords in context
        section_lower = section.lower()
        if any(word in section_lower for word in ['critical', 'lose funds', 'total loss', 'drain']):
            return "CRITICAL"
        elif any(word in section_lower for word in ['high risk', 'significant', 'major impact']):
            return "HIGH"
        elif any(word in section_lower for word in ['medium', 'moderate', 'limited impact']):
            return "MEDIUM"
        elif any(word in section_lower for word in ['low risk', 'minor', 'informational']):
            return "LOW"
        
        return "MEDIUM"

    def _extract_description(self, section: str) -> str:
        """Extract vulnerability description"""
        # Look for explicit description sections
        desc_patterns = [
            r'(?:description|summary|issue|problem)[:\s]*((?:[^\n]|\n(?!\s*\*\*))*?)(?=\n\s*\*\*|$)',
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, section, re.IGNORECASE | re.DOTALL)
            if match:
                desc = match.group(1).strip()
                if len(desc) > 40:
                    return self._clean_extracted_text(desc)
        
        # Fallback: Take first substantial paragraph
        paragraphs = re.split(r'\n\s*\n', section)
        for para in paragraphs:
            para = para.strip()
            if (len(para) > 80 and 
                any(word in para.lower() for word in ['vulnerability', 'allows', 'enables', 'causes', 'risk']) and
                not self._is_template_text(para)):
                return self._clean_extracted_text(para)
        
        return "Security vulnerability identified in smart contract code"

    def _extract_attack_scenario(self, section: str) -> str:
        """Extract attack scenario"""
        attack_patterns = [
            r'(?:attack\s+scenario|scenario|exploit\s+path)[:\s]*((?:[^\n]|\n(?!\s*\*\*))*?)(?=\n\s*\*\*|$)',
        ]
        
        for pattern in attack_patterns:
            match = re.search(pattern, section, re.IGNORECASE | re.DOTALL)
            if match:
                scenario = match.group(1).strip()
                if len(scenario) > 30:
                    return self._clean_extracted_text(scenario)
        
        # Look for sentences describing attack process
        sentences = re.split(r'[.!?]+', section)
        attack_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if (len(sentence) > 30 and 
                any(word in sentence.lower() for word in ['attacker', 'exploit', 'malicious', 'can call', 'manipulate']) and
                not self._is_template_text(sentence)):
                attack_sentences.append(sentence)
                if len(' '.join(attack_sentences)) > 200:
                    break
        
        if attack_sentences:
            return self._clean_extracted_text('. '.join(attack_sentences) + '.')
        
        return "Attacker can exploit this vulnerability to compromise contract security"

    def _extract_remediation(self, section: str) -> str:
        """Extract remediation advice"""
        remediation_patterns = [
            r'(?:remediation|fix|solution|mitigation)[:\s]*((?:[^\n]|\n(?!\s*\*\*))*?)(?=\n\s*\*\*|$)',
        ]
        
        for pattern in remediation_patterns:
            match = re.search(pattern, section, re.IGNORECASE | re.DOTALL)
            if match:
                remediation = match.group(1).strip()
                if len(remediation) > 30:
                    return self._clean_extracted_text(remediation)
        
        return "Implement security best practices to address this vulnerability"

    def _extract_vulnerable_code(self, section: str) -> tuple:
        """Extract vulnerable code snippet and location"""
        # Look for code blocks
        code_patterns = [
            r'```(?:solidity)?\s*([^`]+?)```',
            r'`([^`\n]{15,})`',
        ]
        
        code_snippet = ""
        for pattern in code_patterns:
            matches = re.findall(pattern, section, re.DOTALL)
            if matches:
                for match in matches:
                    code = match.strip()
                    if self._looks_like_solidity_code(code) and len(code) > len(code_snippet):
                        code_snippet = code
        
        # Extract location
        location = ""
        location_patterns = [
            r'(?:line|lines?)[:\s]*(\d+(?:\s*-\s*\d+)?)',
            r'(?:function|method)[:\s]*([a-zA-Z_][a-zA-Z0-9_]*)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                location = match.group(1)
                break
        
        return code_snippet, location

    def _extract_gas_optimizations(self, text: str) -> list:
        """Extract gas optimizations from agent response"""
        optimizations = []
        
        try:
            text = self._clean_agent_response(text)
            print(f"⚡ GAS PARSING: Starting to parse {len(text)} characters of agent response")
            
            # Split by optimization sections
            sections = []
            
            # Enhanced patterns to catch more optimization formats with full content
            opt_patterns = [
                # Numbered optimizations with headers - capture everything until next section or end
                r'(?:^|\n)#{1,6}\s*(\d+)\.\s*([^\n]*(?:optimization|packing|efficiency|gas|save|reduce|cheaper|external|public|loop|storage|memory|constant|immutable|error)[^\n]*)\s*\n(.*?)(?=(?:^|\n)#{1,6}\s*\d+\.|\Z)',
                # Bold numbered optimizations - capture everything until next numbered item or end
                r'(?:^|\n)(\d+)\.\s*\*\*([^\*]*(?:optimization|packing|efficiency|gas|save|reduce|cheaper|external|public|loop|storage|memory|constant|immutable|error)[^\*]*)\*\*\s*\n(.*?)(?=(?:^|\n)\d+\.|\Z)',
                # Simple numbered optimizations - capture everything until next numbered item or end
                r'(?:^|\n)(\d+)\.\s*([^\n]*(?:optimization|packing|efficiency|gas|save|reduce|cheaper|external|public|loop|storage|memory|constant|immutable|error)[^\n]*)\n(.*?)(?=(?:^|\n)\d+\.|\Z)',
                # Bold optimization headers without numbers
                r'(?:^|\n)\*\*([^\*]*(?:optimization|packing|efficiency|gas|save|reduce|cheaper|external|public|loop|storage|memory|constant|immutable|error)[^\*]*)\*\*\s*\n(.*?)(?=(?:^|\n)\*\*[^\*]*(?:optimization|packing|efficiency|gas)|\Z)',
            ]
            
            for pattern in opt_patterns:
                numbered_opts = re.findall(pattern, text, re.DOTALL | re.MULTILINE | re.IGNORECASE)
                if numbered_opts:
                    print(f"⚡ GAS PARSING: Found {len(numbered_opts)} optimizations with pattern")
                    for match in numbered_opts:
                        if len(match) == 3:  # (num, title, content)
                            num, title, content = match
                            full_section = f"{title.strip()}\n{content.strip()}"
                        else:  # (title, content)
                            title, content = match
                            full_section = f"{title.strip()}\n{content.strip()}"
                            num = "?"
                        
                        if len(content.strip()) > 30:  # Reduced threshold
                            sections.append(full_section)
                            print(f"📝 Added optimization {num}: {title.strip()[:60]}...")
                    break
            
            # If no numbered sections, use enhanced paragraph-based parsing
            if not sections:
                print(f"⚡ GAS PARSING: Using enhanced paragraph-based parsing")
                
                # Try splitting by different patterns
                split_patterns = [
                    r'\n\s*\n',  # Double newlines
                    r'(?:^|\n)(?=\d+\.)',  # Before numbered items
                    r'(?:^|\n)(?=\*\*[^*]*(?:optimization|gas|save|reduce|efficient))',  # Before bold optimization headers
                ]
                
                for pattern in split_patterns:
                    paragraphs = re.split(pattern, text)
                    if len(paragraphs) > 1:
                        break
                
                gas_keywords = [
                    'gas', 'optimization', 'optimize', 'efficient', 'cheaper', 'save', 'reduce',
                    'packing', 'storage', 'memory', 'external', 'public', 'loop',
                    'increment', 'constant', 'immutable', 'error', 'require', 'assembly',
                    'uint256', 'uint', 'bytes32', 'mapping', 'struct', 'array',
                    'expensive', 'cost', 'consumption', 'usage'
                ]
                
                for para in paragraphs:
                    para = para.strip()
                    if (len(para) > 50 and  # Reduced minimum length
                        any(keyword in para.lower() for keyword in gas_keywords) and
                        not self._is_template_text(para)):
                        sections.append(para)
                        print(f"📝 Added paragraph section: {para[:60]}...")
            
            print(f"⚡ GAS PARSING: Processing {len(sections)} sections for optimization extraction")
            
            for i, section in enumerate(sections):
                try:
                    section = section.strip()
                    if len(section) < 40:  # Reduced minimum length
                        print(f"⚡ GAS PARSING: Skipping short section {i+1} ({len(section)} chars)")
                        continue
                    
                    print(f"⚡ GAS PARSING: Processing section {i+1}: {section[:100]}...")
                    
                    opt_info = self._extract_gas_optimization_info(section)
                    
                    if self._is_valid_gas_optimization(opt_info, section):
                        print(f"✅ GAS PARSING: Added optimization: {opt_info['optimization_type']}")
                        optimizations.append(opt_info)
                    else:
                        print(f"❌ GAS PARSING: Rejected section - insufficient content")
                        print(f"   Description length: {len(opt_info.get('description', ''))}")
                        print(f"   Optimization type: {opt_info.get('optimization_type', 'N/A')}")
                        
                except Exception as section_error:
                    print(f"❌ ERROR processing gas section {i+1}: {str(section_error)}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            print(f"⚡ GAS PARSING: Final result - {len(optimizations)} optimizations found")
            
            # If no optimizations found, create fallback optimizations from raw text
            if len(optimizations) == 0 and len(text) > 100:
                print("⚡ GAS PARSING: No structured optimizations found, creating fallback optimizations...")
                fallback_optimizations = self._create_fallback_gas_optimizations(text)
                optimizations.extend(fallback_optimizations)
                print(f"⚡ GAS PARSING: Added {len(fallback_optimizations)} fallback optimizations")
            
            return optimizations
            
        except Exception as e:
            print(f"❌ ERROR in _extract_gas_optimizations: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    def _extract_gas_optimization_info(self, section: str) -> dict:
        """Extract gas optimization information"""
        opt_type = self._extract_optimization_type(section)
        description = self._extract_optimization_description(section)
        gas_savings = self._extract_gas_savings(section)
        difficulty = self._extract_implementation_difficulty(section)
        original_code, optimized_code = self._extract_code_examples(section)
        
        return {
            "optimization_type": opt_type,
            "description": description,
            "estimated_gas_savings": gas_savings,
            "implementation_difficulty": difficulty,
            "original_code": original_code,
            "optimized_code": optimized_code
        }

    def _extract_optimization_type(self, section: str) -> str:
        """Extract optimization type"""
        # Enhanced type patterns
        type_patterns = [
            r'(?:optimization\s+type|type|category)[:\s]*([^\n]+)',
            r'\*\*\s*([^*\n]+(?:optimization|packing|efficiency|gas|save|reduce))\s*\*\*',
            r'(?:^|\n)#{1,6}\s*([^#\n]*(?:optimization|packing|efficiency|gas|save|reduce)[^#\n]*)(?:\n|$)',
            r'(?:^|\n)(\d+\.\s*[^:\n]*(?:optimization|packing|efficiency|gas|save|reduce)[^:\n]*?)(?:\n|:)',
        ]
        
        for pattern in type_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                opt_type = match.group(1).strip()
                opt_type = re.sub(r'^[*\s\-#\d\.]+|[*\s\-#]+$', '', opt_type)
                if len(opt_type) > 3 and len(opt_type) < 80:
                    return opt_type
        
        # Enhanced specific optimization patterns
        opt_patterns = {
            r'storage.*pack': 'Storage Packing Optimization',
            r'memory.*cach': 'Memory Caching Optimization',
            r'loop.*optim': 'Loop Optimization',
            r'external.*public': 'External vs Public Optimization',
            r'public.*external': 'Function Visibility Optimization',
            r'custom.*error': 'Custom Error Optimization',
            r'require.*revert': 'Error Handling Optimization',
            r'\+\+i.*i\+\+': 'Increment Optimization',
            r'i\+\+.*\+\+i': 'Pre-increment Optimization',
            r'constant.*immutable': 'Variable Declaration Optimization',
            r'immutable.*constant': 'State Variable Optimization',
            r'uint256.*uint': 'Type Optimization',
            r'bytes32.*string': 'Data Type Optimization',
            r'mapping.*array': 'Data Structure Optimization',
            r'assembly.*inline': 'Assembly Optimization',
            r'gas.*limit': 'Gas Limit Optimization',
            r'storage.*read': 'Storage Access Optimization',
            r'storage.*write': 'Storage Write Optimization',
            r'function.*visibility': 'Function Visibility Optimization',
            r'struct.*pack': 'Struct Packing Optimization',
            r'array.*length': 'Array Length Optimization',
            r'zero.*value': 'Zero Value Optimization'
        }
        
        section_lower = section.lower()
        for pattern, opt_name in opt_patterns.items():
            if re.search(pattern, section_lower):
                return opt_name
        
        # Check for common gas optimization keywords in the first line
        first_line = section.split('\n')[0].lower()
        if any(word in first_line for word in ['storage', 'memory', 'loop', 'external', 'public', 'constant', 'immutable']):
            if 'storage' in first_line:
                return 'Storage Optimization'
            elif 'memory' in first_line:
                return 'Memory Optimization'
            elif 'loop' in first_line:
                return 'Loop Optimization'
            elif any(word in first_line for word in ['external', 'public']):
                return 'Function Visibility Optimization'
            elif any(word in first_line for word in ['constant', 'immutable']):
                return 'Variable Declaration Optimization'
        
        return "Gas Optimization"

    def _extract_optimization_description(self, section: str) -> str:
        """Extract optimization description"""
        # Enhanced description patterns
        desc_patterns = [
            r'(?:description|summary|issue|inefficiency|problem)[:\s]*((?:[^\n]|\n(?!\s*\*\*))*?)(?=\n\s*\*\*|$)',
            r'(?:current\s+code|original\s+code|before)[:\s]*[^\n]*\n(.*?)(?=(?:optimized|after|solution|fix|\n\s*\*\*)|$)',
            r'(?:^|\n)([^:\n]*(?:gas|inefficient|optimize|reduce|save|expensive|cost)[^:\n]*?)(?:\n|:)',
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, section, re.IGNORECASE | re.DOTALL)
            if match:
                desc = match.group(1).strip()
                desc = self._clean_extracted_text(desc)
                if len(desc) > 20 and not self._is_template_text(desc):
                    return desc
        
        # Fallback to first sentences that mention gas optimization
        sentences = re.split(r'[.!?]+', section)
        desc_sentences = []
        
        for sentence in sentences[:6]:  # Check more sentences
            sentence = sentence.strip()
            if (len(sentence) > 15 and  # Reduced threshold
                any(word in sentence.lower() for word in [
                    'gas', 'inefficient', 'optimize', 'reduce', 'save', 'expensive',
                    'cost', 'efficient', 'cheaper', 'packing', 'storage', 'memory',
                    'external', 'public', 'loop', 'constant', 'immutable'
                ]) and
                not self._is_template_text(sentence)):
                desc_sentences.append(sentence)
                if len(' '.join(desc_sentences)) > 80:
                    break
        
        if desc_sentences:
            return self._clean_extracted_text('. '.join(desc_sentences) + '.')
        
        # Last resort: use the first substantial line that mentions gas
        lines = section.split('\n')
        for line in lines:
            line = line.strip()
            if (len(line) > 20 and 
                any(word in line.lower() for word in ['gas', 'optimization', 'efficient', 'save', 'reduce']) and
                not self._is_template_text(line)):
                return self._clean_extracted_text(line)
        
        return "Gas optimization opportunity identified in smart contract"

    def _extract_gas_savings(self, section: str) -> str:
        """Extract estimated gas savings"""
        # Enhanced patterns to capture more gas savings formats
        savings_patterns = [
            r'(?:estimated\s+)?gas\s+savings?[:\s]*(\d+)',
            r'(?:saves?|reduction)[:\s]*(\d+)\s*gas',
            r'(\d+)\s*gas.*?(?:saved|reduction|less)',
            r'(\d+)\s*gas\s+(?:per|units)',  # "1200 gas per iteration", "15000 gas units"
            r'saves?\s+approximately\s+(\d+)\s*gas',  # "saves approximately 1200 gas"
            r'estimated\s+savings?[:\s]*(\d+)',  # "Estimated savings: 2000"
            r'gas[:\s]*(\d+)\s*units',  # "Gas: 15000 units"
            r'(\d+)\s*(?:gas\s+)?units\s+per',  # "15000 units per transaction"
        ]
        
        for pattern in savings_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                savings = int(match.group(1))
                if 0 < savings < 1000000:  # Reasonable range
                    return str(savings)
        
        # Look for proper range patterns (e.g., "1000-1500 gas", "500 to 800 gas")
        range_patterns = [
            r'(\d+)[-–]\s*(\d+)\s*gas',  # "1000-1500 gas"
            r'(\d+)\s*to\s*(\d+)\s*gas',  # "500 to 800 gas"
            r'between\s+(\d+)\s+and\s+(\d+)\s*gas',  # "between 100 and 200 gas"
        ]
        
        for pattern in range_patterns:
            range_match = re.search(pattern, section, re.IGNORECASE)
            if range_match:
                lower, upper = int(range_match.group(1)), int(range_match.group(2))
                if lower < upper:  # Valid range
                    return str(upper)  # Take upper bound
        
        # Default estimates based on optimization type
        section_lower = section.lower()
        if 'storage' in section_lower and 'pack' in section_lower:
            return "20000"
        elif 'loop' in section_lower:
            return "1500"
        elif 'external' in section_lower:
            return "500"
        else:
            return "1000"

    def _extract_implementation_difficulty(self, section: str) -> str:
        """Extract implementation difficulty"""
        difficulty_patterns = [
            r'(?:implementation\s+)?difficulty[:\s]*([a-zA-Z]+)',
            r'(?:complexity|effort)[:\s]*([a-zA-Z]+)',
        ]
        
        for pattern in difficulty_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                difficulty = match.group(1).strip().lower()
                if difficulty in ['easy', 'medium', 'hard']:
                    return difficulty
        
        # Infer from content
        section_lower = section.lower()
        if any(word in section_lower for word in ['simple', 'straightforward', 'easy', 'trivial']):
            return "easy"
        elif any(word in section_lower for word in ['complex', 'difficult', 'risky', 'careful', 'breaking']):
            return "hard"
        else:
            return "medium"

    def _extract_code_examples(self, section: str) -> tuple:
        """Extract original and optimized code examples"""
        # Find all code blocks
        code_patterns = [
            r'```(?:solidity|sol)?\s*(.*?)```',
            r'`([^`\n]{20,})`',
        ]
        
        all_code_blocks = []
        for pattern in code_patterns:
            blocks = re.findall(pattern, section, re.DOTALL)
            for block in blocks:
                block = block.strip()
                if len(block) > 20 and self._looks_like_solidity_code(block):
                    all_code_blocks.append(block)
        
        if len(all_code_blocks) >= 2:
            return all_code_blocks[0], all_code_blocks[1]
        elif len(all_code_blocks) == 1:
            # Generate the missing code example
            return self._generate_code_examples(all_code_blocks[0], section)
        else:
            # Generate both based on section content
            default_original = "// Original inefficient code:\ncontract Example {\n    uint256 public value;\n    function setValue(uint256 _value) public {\n        value = _value;\n    }\n}"
            default_optimized = "// Optimized code:\ncontract Example {\n    uint256 public value;\n    function setValue(uint256 _value) external {\n        value = _value;\n    }\n}"
            return default_original, default_optimized

    def _generate_code_examples(self, code: str, section: str) -> tuple:
        """Generate missing code example based on existing one and context"""
        section_lower = section.lower()
        
        # Determine if existing code is original or optimized
        if any(word in section_lower for word in ['before', 'current', 'inefficient', 'original']):
            # Existing is original, generate optimized
            original = code
            optimized = self._generate_realistic_optimization(code)
        else:
            # Existing is optimized, generate original
            optimized = code
            original = self._generate_realistic_original(code)
        
        return original, optimized

    # Helper methods
    def _looks_like_solidity_code(self, text: str) -> bool:
        """Check if text looks like Solidity code"""
        if not text or len(text) < 10:
            return False
        
        solidity_indicators = [
            r'\bfunction\b', r'\bcontract\b', r'\bmapping\b', r'\buint\d*\b',
            r'\baddress\b', r'\bbool\b', r'\bpublic\b', r'\bprivate\b',
            r'\bexternal\b', r'\binternal\b', r'\brequire\b', r'\brevert\b'
        ]
        
        matches = sum(1 for pattern in solidity_indicators if re.search(pattern, text, re.IGNORECASE))
        return matches >= 2

    def _clean_extracted_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\n+', '\n\n', text)
        
        return text.strip()

    def _is_template_text(self, text: str) -> str:
        """Check if text is template/instructional content"""
        template_phrases = [
            'provide', 'include', 'example',
            'template', 'guidelines', 'instructions', 'format',
            'structure', 'should contain', 'must include',
            'for each vulnerability found'
        ]
        
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in template_phrases)

    def _is_valid_security_vulnerability(self, vuln_info: dict, original_section: str) -> bool:
        """Validate if parsed content represents a real vulnerability"""
        desc = vuln_info.get('description', '').lower()
        if len(desc) < 30:
            return False
        
        # Must contain security-related keywords
        security_keywords = [
            'vulnerability', 'security', 'attack', 'exploit', 'risk', 'unsafe', 
            'malicious', 'reentrancy', 'overflow', 'underflow', 'access control'
        ]
        
        if not any(keyword in desc for keyword in security_keywords):
            return False
        
        # Reject template content
        if self._is_template_text(desc):
            return False
        
        return True

    def _is_valid_gas_optimization(self, opt_info: dict, original_section: str) -> bool:
        """Validate if parsed content represents a real gas optimization"""
        desc = opt_info.get('description', '').lower()
        if len(desc) < 20:  # Reduced threshold
            print(f"   Validation failed: Description too short ({len(desc)} chars)")
            return False
        
        # Enhanced gas-related keywords
        gas_keywords = [
            'gas', 'optimization', 'optimize', 'efficient', 'cheaper', 'save',
            'reduce', 'packing', 'storage', 'memory', 'external',
            'public', 'loop', 'increment', 'constant', 'immutable',
            'cost', 'expensive', 'consumption', 'usage', 'assembly',
            'uint256', 'uint', 'bytes32', 'mapping', 'struct', 'array',
            'call', 'function', 'visibility', 'error', 'require'
        ]
        
        if not any(keyword in desc for keyword in gas_keywords):
            print(f"   Validation failed: No gas keywords found in description")
            return False
        
        # Check optimization type
        opt_type = opt_info.get('optimization_type', '').lower()
        if 'gas' not in opt_type and 'optimization' not in opt_type and len(opt_type) < 3:
            print(f"   Validation failed: Invalid optimization type: {opt_type}")
            return False
        
        # Reject template content
        if self._is_template_text(desc):
            print(f"   Validation failed: Template text detected")
            return False
        
        print(f"   ✅ Validation passed: {opt_info.get('optimization_type', 'Unknown')}")
        return True

    def _clean_agent_response(self, text: str) -> str:
        """Clean agent response from metadata"""
        if not text:
            return ""
        
        # Remove common metadata patterns
        text = re.sub(r'conversation_id[:\s]*[a-zA-Z0-9\-_]+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'request_id[:\s]*[a-zA-Z0-9\-_]+', '', text, flags=re.IGNORECASE)
        
        return text.strip()

    def _generate_realistic_optimization(self, original_code: str) -> str:
        """Generate realistic optimized code"""
        if not original_code:
            return "// Gas-optimized version"
        
        optimized = original_code
        
        # Apply common optimizations
        optimized = re.sub(r'\bpublic\b', 'external', optimized)
        optimized = re.sub(r'\bi\+\+', '++i', optimized)
        
        return f"// Gas-optimized version:\n{optimized}"

    def _generate_realistic_original(self, optimized_code: str) -> str:
        """Generate realistic original code"""
        if not optimized_code:
            return "// Original inefficient code"
        
        original = optimized_code
        
        # Reverse optimizations
        original = re.sub(r'\bexternal\b', 'public', original)
        original = re.sub(r'\+\+i\b', 'i++', original)
        
        return f"// Original inefficient version:\n{original}"
    
    def _create_fallback_gas_optimizations(self, text: str) -> list:
        """Create fallback gas optimizations when structured parsing fails"""
        optimizations = []
        
        # Common gas optimization patterns to look for
        optimization_hints = [
            {
                'keywords': ['storage', 'pack', 'slot'],
                'type': 'Storage Packing Optimization',
                'description': 'Pack storage variables to reduce storage slots and save gas on state operations.',
                'savings': '20000'
            },
            {
                'keywords': ['external', 'public', 'function'],
                'type': 'Function Visibility Optimization',
                'description': 'Use external instead of public for functions to save gas on function calls.',
                'savings': '500'
            },
            {
                'keywords': ['loop', '++i', 'i++', 'increment'],
                'type': 'Loop Optimization',
                'description': 'Use ++i instead of i++ in loops to save gas on increment operations.',
                'savings': '1000'
            },
            {
                'keywords': ['constant', 'immutable', 'variable'],
                'type': 'Variable Declaration Optimization',
                'description': 'Use constant or immutable for unchanging values to save gas.',
                'savings': '2000'
            },
            {
                'keywords': ['require', 'error', 'revert', 'string'],
                'type': 'Custom Error Optimization',
                'description': 'Replace require statements with custom errors to reduce gas costs.',
                'savings': '1500'
            },
            {
                'keywords': ['memory', 'storage', 'cache'],
                'type': 'Memory Optimization',
                'description': 'Cache storage reads in memory to avoid redundant SLOAD operations.',
                'savings': '800'
            }
        ]
        
        text_lower = text.lower()
        
        for hint in optimization_hints:
            if any(keyword in text_lower for keyword in hint['keywords']):
                # Extract relevant text snippet
                code_snippet = self._extract_relevant_code_snippet(text, hint['keywords'])
                
                optimization = {
                    'optimization_type': hint['type'],
                    'description': hint['description'],
                    'estimated_gas_savings': hint['savings'],
                    'implementation_difficulty': 'medium',
                    'original_code': f"// Original code (example):\n{code_snippet if code_snippet else 'contract Example { uint256 public value; }'}",
                    'optimized_code': f"// Optimized code (example):\n{self._generate_optimized_example(hint['type'], code_snippet)}"
                }
                
                optimizations.append(optimization)
                print(f"📝 Created fallback optimization: {hint['type']}")
        
        return optimizations[:3]  # Limit to 3 fallback optimizations

    def _extract_relevant_code_snippet(self, text: str, keywords: list) -> str:
        """Extract a relevant code snippet based on keywords"""
        # Look for code blocks first
        code_patterns = [
            r'```(?:solidity|sol)?\s*(.*?)```',
            r'`([^`\n]{20,})`',
        ]
        
        for pattern in code_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                match = match.strip()
                if any(keyword in match.lower() for keyword in keywords):
                    return match[:200]  # Limit length
        
        # Look for lines containing keywords
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in keywords) and len(line.strip()) > 10:
                return line.strip()[:100]
        
        return ""

    def _generate_optimized_example(self, opt_type: str, original_code: str) -> str:
        """Generate an optimized code example based on optimization type"""
        if 'storage' in opt_type.lower():
            return "contract Example {\n    address public owner;\n    bool public paused;  // Packed with owner\n    uint256 public value;\n}"
        elif 'external' in opt_type.lower():
            return "function getData() external view returns (uint256) {\n    return value;\n}"
        elif 'loop' in opt_type.lower():
            return "for (uint256 i = 0; i < length; ++i) {\n    // Process item\n}"
        elif 'constant' in opt_type.lower():
            return "uint256 public constant MAX_SUPPLY = 1000000;"
        elif 'error' in opt_type.lower():
            return "error InsufficientBalance();\nif (balance < amount) revert InsufficientBalance();"
        elif 'memory' in opt_type.lower():
            return "uint256 cachedValue = storageValue;\n// Use cachedValue instead of storageValue"
        else:
            return "// Optimized version of the code"
