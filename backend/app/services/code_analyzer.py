"""
Code Analyzer Service
AI-powered code security analysis using Claude/GPT
"""

import uuid
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
import structlog
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas.analysis import (
    CodeAnalysisResponse,
    Vulnerability,
    VulnerabilityLocation,
    SeveritySummary,
    ComplianceStatus,
    DependencyVulnerability,
    Secret
)
from app.services.prompts import CODE_ANALYSIS_PROMPT

logger = structlog.get_logger(__name__)


class CodeAnalyzerService:
    """
    Service for analyzing code security using AI models
    """

    def __init__(self):
        self.anthropic_client = None
        self.openai_client = None

        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze(
        self,
        code: str,
        language: str,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive security analysis on code

        Args:
            code: Source code to analyze
            language: Programming language
            filename: Optional filename

        Returns:
            Analysis results with vulnerabilities, secrets, and recommendations
        """
        try:
            logger.info("Starting code analysis", language=language)

            # Generate analysis ID
            analysis_id = str(uuid.uuid4())

            # Build prompt
            prompt = self._build_analysis_prompt(code, language, filename)

            # Call AI model
            ai_response = await self._call_ai_model(prompt)

            # Parse AI response
            parsed_results = self._parse_ai_response(ai_response)

            # Run additional security tools (semgrep, bandit, etc.)
            tool_results = await self._run_security_tools(code, language)

            # Merge results
            final_results = self._merge_results(parsed_results, tool_results)

            # Add metadata
            final_results.update({
                "analysis_id": analysis_id,
                "timestamp": datetime.utcnow().isoformat(),
                "language": language,
                "metadata": {
                    "code_hash": hashlib.sha256(code.encode()).hexdigest(),
                    "lines_of_code": code.count('\n') + 1,
                    "analyzer_version": "1.0.0"
                }
            })

            return final_results

        except Exception as e:
            logger.error("Code analysis failed", error=str(e), exc_info=True)
            raise

    def _build_analysis_prompt(
        self,
        code: str,
        language: str,
        filename: Optional[str]
    ) -> str:
        """
        Build the analysis prompt for the AI model
        """
        return CODE_ANALYSIS_PROMPT.format(
            language=language,
            code=code,
            filename=filename or "unknown"
        )

    async def _call_ai_model(self, prompt: str) -> str:
        """
        Call the configured AI model (Claude or GPT)
        """
        try:
            if self.anthropic_client:
                logger.debug("Using Claude for analysis")
                response = await self.anthropic_client.messages.create(
                    model=settings.AI_MODEL_CODE,
                    max_tokens=settings.AI_MAX_TOKENS,
                    temperature=settings.AI_TEMPERATURE,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                return response.content[0].text

            elif self.openai_client:
                logger.debug("Using GPT for analysis")
                response = await self.openai_client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a security expert analyzing code for vulnerabilities."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=settings.AI_TEMPERATURE,
                    max_tokens=settings.AI_MAX_TOKENS
                )
                return response.choices[0].message.content

            else:
                raise ValueError("No AI API key configured")

        except Exception as e:
            logger.error("AI model call failed", error=str(e))
            raise

    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """
        Parse AI response into structured format

        The AI is expected to return JSON with vulnerabilities, secrets, etc.
        """
        import json

        try:
            # Extract JSON from response (in case it's wrapped in markdown)
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()

            data = json.loads(response)

            # Validate and structure the response
            vulnerabilities = []
            for vuln in data.get("vulnerabilities", []):
                vulnerabilities.append({
                    "id": vuln.get("id", "UNKNOWN"),
                    "title": vuln.get("title", "Unknown Vulnerability"),
                    "severity": vuln.get("severity", "MEDIUM").upper(),
                    "confidence": vuln.get("confidence", 0.8),
                    "description": vuln.get("description", ""),
                    "impact": vuln.get("impact", ""),
                    "exploitability": vuln.get("exploitability", "MEDIUM"),
                    "remediation": vuln.get("remediation", ""),
                    "location": vuln.get("location"),
                    "secure_code": vuln.get("secure_code"),
                    "references": vuln.get("references", [])
                })

            # Calculate summary
            summary = {
                "total_issues": len(vulnerabilities),
                "critical": sum(1 for v in vulnerabilities if v["severity"] == "CRITICAL"),
                "high": sum(1 for v in vulnerabilities if v["severity"] == "HIGH"),
                "medium": sum(1 for v in vulnerabilities if v["severity"] == "MEDIUM"),
                "low": sum(1 for v in vulnerabilities if v["severity"] == "LOW"),
                "info": sum(1 for v in vulnerabilities if v["severity"] == "INFO")
            }

            return {
                "vulnerabilities": vulnerabilities,
                "summary": summary,
                "secrets": data.get("secrets", []),
                "dependencies": data.get("dependencies", []),
                "compliance": data.get("compliance", {})
            }

        except json.JSONDecodeError as e:
            logger.error("Failed to parse AI response as JSON", error=str(e))
            # Return empty results if parsing fails
            return {
                "vulnerabilities": [],
                "summary": {
                    "total_issues": 0,
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                    "info": 0
                },
                "secrets": [],
                "dependencies": [],
                "compliance": {}
            }

    async def _run_security_tools(
        self,
        code: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Run additional security analysis tools (semgrep, bandit, etc.)

        This is a placeholder for integration with static analysis tools
        """
        # TODO: Integrate with actual security tools
        # - Semgrep for pattern matching
        # - Bandit for Python
        # - ESLint security rules for JavaScript
        # - etc.

        logger.debug("Running security tools", language=language)

        return {
            "tool_vulnerabilities": [],
            "tool_secrets": []
        }

    def _merge_results(
        self,
        ai_results: Dict[str, Any],
        tool_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge AI analysis results with tool results
        """
        # Merge vulnerabilities
        all_vulns = ai_results.get("vulnerabilities", [])
        all_vulns.extend(tool_results.get("tool_vulnerabilities", []))

        # Merge secrets
        all_secrets = ai_results.get("secrets", [])
        all_secrets.extend(tool_results.get("tool_secrets", []))

        # Recalculate summary
        summary = {
            "total_issues": len(all_vulns),
            "critical": sum(1 for v in all_vulns if v.get("severity") == "CRITICAL"),
            "high": sum(1 for v in all_vulns if v.get("severity") == "HIGH"),
            "medium": sum(1 for v in all_vulns if v.get("severity") == "MEDIUM"),
            "low": sum(1 for v in all_vulns if v.get("severity") == "LOW"),
            "info": sum(1 for v in all_vulns if v.get("severity") == "INFO")
        }

        return {
            "vulnerabilities": all_vulns,
            "summary": summary,
            "secrets": all_secrets,
            "dependencies": ai_results.get("dependencies", []),
            "compliance": ai_results.get("compliance", {})
        }
