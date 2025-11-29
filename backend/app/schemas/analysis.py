"""
Analysis Schemas
Pydantic models for analysis requests and responses
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class CodeAnalysisRequest(BaseModel):
    """
    Code analysis request schema
    """
    code: str = Field(..., min_length=1, max_length=1_000_000)
    language: str = Field(..., min_length=1, max_length=50)
    filename: Optional[str] = Field(None, max_length=255)

    @field_validator("language")
    @classmethod
    def validate_language(cls, v):
        """Normalize language name"""
        return v.lower().strip()


class VulnerabilityLocation(BaseModel):
    """Location of a vulnerability in code"""
    file: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    snippet: Optional[str] = None


class Vulnerability(BaseModel):
    """Security vulnerability details"""
    id: str = Field(..., description="CWE or vulnerability ID")
    title: str = Field(..., description="Vulnerability title")
    severity: str = Field(..., description="Severity level")
    confidence: float = Field(..., ge=0.0, le=1.0)
    description: str
    impact: str
    exploitability: str
    remediation: str
    location: Optional[VulnerabilityLocation] = None
    secure_code: Optional[str] = None
    references: List[str] = Field(default_factory=list)


class DependencyVulnerability(BaseModel):
    """Dependency vulnerability"""
    name: str
    version: str
    vulnerabilities: int
    severity: str
    recommendation: Optional[str] = None


class Secret(BaseModel):
    """Detected secret"""
    type: str
    line: int
    description: str


class ComplianceStatus(BaseModel):
    """Compliance framework status"""
    compliant: bool
    issues: int = 0
    details: Optional[str] = None


class SeveritySummary(BaseModel):
    """Summary of vulnerabilities by severity"""
    total_issues: int = 0
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    info: int = 0


class CodeAnalysisResponse(BaseModel):
    """
    Code analysis response schema
    """
    analysis_id: str
    timestamp: str
    language: str
    vulnerabilities: List[Vulnerability]
    summary: SeveritySummary
    dependencies: List[DependencyVulnerability] = Field(default_factory=list)
    secrets: List[Secret] = Field(default_factory=list)
    compliance: Dict[str, ComplianceStatus] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ArchitectureComponent(BaseModel):
    """Identified architecture component"""
    name: str
    type: str
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    security_controls: List[str] = Field(default_factory=list)


class SecurityWeakness(BaseModel):
    """Security weakness in architecture"""
    title: str
    severity: str
    description: str
    affected_components: List[str] = Field(default_factory=list)
    recommendation: str
    references: List[str] = Field(default_factory=list)


class SecurityAssessment(BaseModel):
    """Overall security assessment"""
    overall: str
    risk_level: str
    strengths: List[str] = Field(default_factory=list)
    concerns: List[str] = Field(default_factory=list)


class ZeroTrustProposal(BaseModel):
    """Zero Trust architecture recommendations"""
    network_segmentation: Optional[List[str]] = None
    identity_access: Optional[List[str]] = None
    encryption: Optional[List[str]] = None
    monitoring: Optional[List[str]] = None


class SecureByDesign(BaseModel):
    """Secure-by-design recommendations"""
    hardening: Optional[List[str]] = None
    redundancy: Optional[List[str]] = None
    data_protection: Optional[List[str]] = None
    best_practices: Optional[List[str]] = None


class DiagramAnalysisResponse(BaseModel):
    """
    Diagram analysis response schema
    """
    analysis_id: str
    timestamp: str
    components: List[ArchitectureComponent]
    security_assessment: SecurityAssessment
    weaknesses: List[SecurityWeakness]
    zero_trust_proposal: ZeroTrustProposal
    secure_by_design: SecureByDesign
    compliance: Dict[str, ComplianceStatus]
    metadata: Dict[str, Any] = Field(default_factory=dict)
