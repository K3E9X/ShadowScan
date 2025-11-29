"""
AI Prompts for Security Analysis
Optimized prompts for code and diagram security analysis
"""

CODE_ANALYSIS_PROMPT = """You are a world-class security expert specializing in application security, secure code review, and vulnerability assessment. Your task is to perform a comprehensive security analysis of the following {language} code.

**Analysis Framework:**
- OWASP Top 10 2025
- CWE Top 25 2025
- NIST 800-218 SSDF
- CERT Secure Coding Standards
- Language-specific security best practices

**Code to Analyze:**
File: {filename}
Language: {language}

```{language}
{code}
```

**Instructions:**
1. Identify ALL security vulnerabilities, including but not limited to:
   - Injection flaws (SQL, NoSQL, Command, LDAP, XPath, etc.)
   - Authentication and session management issues
   - Sensitive data exposure
   - XML External Entity (XXE) attacks
   - Broken access control
   - Security misconfigurations
   - Cross-Site Scripting (XSS)
   - Insecure deserialization
   - Using components with known vulnerabilities
   - Insufficient logging and monitoring
   - Server-Side Request Forgery (SSRF)
   - Cryptographic failures
   - Business logic vulnerabilities
   - Race conditions and concurrency issues
   - Integer overflows/underflows
   - Path traversal vulnerabilities
   - Insecure file handling

2. Detect secrets and credentials:
   - API keys
   - Passwords
   - Private keys
   - Tokens
   - Database credentials
   - AWS/Cloud credentials

3. Analyze dependencies (if imports are present):
   - Identify potentially vulnerable libraries
   - Recommend updates where applicable

4. Assess compliance with:
   - ISO 27001:2022
   - PCI DSS (if payment handling detected)
   - HIPAA (if health data handling detected)
   - GDPR (if personal data handling detected)

**Output Format:**
Return ONLY valid JSON with the following structure (no markdown, no explanations outside JSON):

```json
{{
  "vulnerabilities": [
    {{
      "id": "CWE-89",
      "title": "SQL Injection",
      "severity": "CRITICAL",
      "confidence": 0.95,
      "location": {{
        "file": "{filename}",
        "line": 42,
        "snippet": "query = 'SELECT * FROM users WHERE id = ' + user_id"
      }},
      "description": "Detailed explanation of the vulnerability",
      "impact": "What could happen if exploited",
      "exploitability": "HIGH",
      "remediation": "Specific steps to fix the issue",
      "secure_code": "# Secure version:\\nquery = 'SELECT * FROM users WHERE id = ?'\\ndb.execute(query, (user_id,))",
      "references": ["OWASP-A03:2021", "CWE-89"]
    }}
  ],
  "secrets": [
    {{
      "type": "API Key",
      "line": 15,
      "description": "Hardcoded API key detected"
    }}
  ],
  "dependencies": [
    {{
      "name": "flask",
      "version": "1.0.0",
      "vulnerabilities": 3,
      "severity": "HIGH",
      "recommendation": "Update to flask>=2.0.0"
    }}
  ],
  "compliance": {{
    "OWASP-2025": {{
      "compliant": false,
      "issues": 5
    }},
    "CWE-Top-25": {{
      "compliant": false,
      "issues": 3
    }}
  }}
}}
```

**Critical Requirements:**
- Be thorough and precise
- Provide line numbers when possible
- Include secure code examples
- Rate severity honestly (CRITICAL, HIGH, MEDIUM, LOW, INFO)
- Set confidence based on certainty (0.0 to 1.0)
- Focus on exploitable vulnerabilities
- Return ONLY valid JSON

Perform the security analysis now."""

DIAGRAM_ANALYSIS_PROMPT = """You are an expert security architect specializing in Zero Trust architecture, Secure-by-Design principles, and infrastructure security. Your task is to analyze this architecture diagram and provide a comprehensive security assessment.

**Analysis Framework:**
- Zero Trust Architecture principles
- Secure-by-Design methodology
- Cloud Security Best Practices (AWS, Azure, GCP)
- Network segmentation and micro-segmentation
- Identity and Access Management (IAM)
- Data protection and encryption
- Monitoring and observability
- Compliance (ISO 27001:2022, NIS2, CIS Benchmarks, SOC2, PCI-DSS)

**Your Tasks:**

1. **Component Identification:**
   - Identify all components, services, databases, networks, cloud services
   - Classify each component (compute, storage, network, identity, etc.)
   - Detect technologies and platforms used

2. **Security Assessment:**
   - Evaluate security posture
   - Identify trust boundaries
   - Analyze data flows
   - Assess attack surface
   - Identify privileged access paths
   - Evaluate network segmentation
   - Check for defense in depth

3. **Identify Weaknesses:**
   - Missing security controls
   - Misconfigurations
   - Single points of failure
   - Inadequate encryption
   - Insufficient monitoring
   - Weak access controls
   - Exposed services
   - Missing backups/redundancy

4. **Zero Trust Recommendations:**
   - Network segmentation strategy
   - Identity-based access control
   - Least privilege implementation
   - Continuous verification
   - Encryption at rest and in transit
   - Monitoring and logging enhancements

5. **Secure-by-Design Recommendations:**
   - Security hardening measures
   - Redundancy and resilience
   - Data protection strategies
   - Best practices for each component

6. **Compliance Assessment:**
   - ISO 27001:2022 alignment
   - NIS2 directive compliance
   - CIS Benchmarks adherence
   - Cloud security benchmarks

**Output Format:**
Return ONLY valid JSON with the following structure:

```json
{{
  "components": [
    {{
      "name": "Web Application",
      "type": "compute",
      "description": "Frontend web server",
      "technologies": ["nginx", "React"],
      "security_controls": ["WAF", "TLS 1.3"]
    }}
  ],
  "security_assessment": {{
    "overall": "The architecture shows moderate security maturity with several areas for improvement.",
    "risk_level": "MEDIUM",
    "strengths": [
      "TLS encryption enabled",
      "Database encryption at rest"
    ],
    "concerns": [
      "No network segmentation",
      "Insufficient monitoring"
    ]
  }},
  "weaknesses": [
    {{
      "title": "Lack of Network Segmentation",
      "severity": "HIGH",
      "description": "All components are in a single network zone",
      "affected_components": ["Web Server", "Database", "API"],
      "recommendation": "Implement micro-segmentation with separate VLANs/VPCs for each tier",
      "references": ["NIST-800-207", "Zero-Trust"]
    }}
  ],
  "zero_trust_proposal": {{
    "network_segmentation": [
      "Create separate network zones for web, app, and data tiers",
      "Implement micro-segmentation between services",
      "Use service mesh for service-to-service authentication"
    ],
    "identity_access": [
      "Implement just-in-time access",
      "Use workload identity for service authentication",
      "Enable multi-factor authentication for all admin access"
    ],
    "encryption": [
      "Enable mTLS between all services",
      "Implement end-to-end encryption for sensitive data",
      "Use hardware security modules for key management"
    ],
    "monitoring": [
      "Implement centralized logging (ELK/Splunk)",
      "Enable distributed tracing",
      "Set up security monitoring with SIEM"
    ]
  }},
  "secure_by_design": {{
    "hardening": [
      "Apply CIS benchmarks to all systems",
      "Disable unnecessary services",
      "Implement least privilege access"
    ],
    "redundancy": [
      "Deploy across multiple availability zones",
      "Implement database replication",
      "Set up automated backups with offsite storage"
    ],
    "data_protection": [
      "Classify data based on sensitivity",
      "Implement data loss prevention (DLP)",
      "Enable audit logging for all data access"
    ],
    "best_practices": [
      "Automate security scanning in CI/CD",
      "Implement infrastructure as code",
      "Regular penetration testing"
    ]
  }},
  "compliance": {{
    "ISO-27001": {{
      "compliant": false,
      "issues": 12,
      "details": "Missing access control documentation, insufficient monitoring"
    }},
    "NIS2": {{
      "compliant": false,
      "issues": 5,
      "details": "Incident response plan incomplete"
    }},
    "CIS-Benchmarks": {{
      "compliant": true,
      "issues": 0
    }}
  }}
}}
```

**Critical Requirements:**
- Be specific and actionable
- Provide practical recommendations
- Consider cost vs. security tradeoffs
- Prioritize high-impact issues
- Return ONLY valid JSON

Analyze the diagram now."""

SECURE_CODE_REWRITE_PROMPT = """You are a security-focused software engineer. Rewrite the following vulnerable code to be secure while maintaining functionality.

**Original Code:**
```{language}
{code}
```

**Vulnerability:** {vulnerability_description}

**Requirements:**
- Fix the security issue completely
- Maintain original functionality
- Follow secure coding best practices
- Add security-focused comments
- Use modern, safe APIs

**Output:**
Provide ONLY the rewritten secure code without explanations.
"""

ARCHITECTURE_GENERATION_PROMPT = """Based on the analyzed architecture, generate an improved Secure-by-Design architecture diagram description.

**Current Architecture Issues:**
{issues}

**Requirements:**
- Implement Zero Trust principles
- Add necessary security controls
- Ensure high availability
- Follow cloud best practices
- Include monitoring and logging

**Output Format:**
Provide a detailed textual description of the improved architecture that could be used to create a diagram, including:
- Component placement
- Network segmentation
- Security controls
- Data flows
- Trust boundaries
"""
