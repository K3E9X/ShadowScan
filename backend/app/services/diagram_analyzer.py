"""
Diagram Analyzer Service
AI-powered architecture diagram analysis using Ollama LLaVA (Local & Free)
"""

import uuid
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
import structlog

from app.core.config import settings
from app.services.prompts import DIAGRAM_ANALYSIS_PROMPT
from app.services.ollama_service import OllamaService

logger = structlog.get_logger(__name__)


class DiagramAnalyzerService:
    """
    Service for analyzing architecture diagrams using Ollama LLaVA vision model
    """

    def __init__(self):
        self.ollama = OllamaService(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL_VISION
        )

    async def analyze(
        self,
        file_content: bytes,
        filename: str,
        content_type: str
    ) -> Dict[str, Any]:
        """
        Perform security analysis on architecture diagram using Ollama LLaVA

        Args:
            file_content: Image file bytes
            filename: Original filename
            content_type: MIME type

        Returns:
            Analysis results with components, weaknesses, and recommendations
        """
        try:
            logger.info(
                "Starting diagram analysis with Ollama LLaVA",
                filename=filename,
                content_type=content_type
            )

            # Generate analysis ID
            analysis_id = str(uuid.uuid4())

            # Convert image to base64 for Ollama
            image_b64 = base64.b64encode(file_content).decode('utf-8')

            # Build prompt
            prompt = DIAGRAM_ANALYSIS_PROMPT

            # Call Ollama vision model
            ai_response = await self._call_vision_model(prompt, image_b64)

            # Parse AI response
            results = self._parse_ai_response(ai_response)

            # Add metadata
            results.update({
                "analysis_id": analysis_id,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {
                    "filename": filename,
                    "file_size": len(file_content),
                    "content_type": content_type,
                    "analyzer_version": "1.0.0",
                    "ai_model": settings.OLLAMA_MODEL_VISION
                }
            })

            return results

        except Exception as e:
            logger.error("Diagram analysis failed", error=str(e), exc_info=True)
            raise

    async def _call_vision_model(
        self,
        prompt: str,
        image_b64: str
    ) -> str:
        """
        Call Ollama LLaVA vision model
        """
        try:
            logger.debug("Using Ollama LLaVA for diagram analysis")

            # System prompt for architecture analysis
            system_prompt = """You are an expert security architect specializing in Zero Trust architecture,
Secure-by-Design principles, and infrastructure security. You have deep knowledge of cloud security,
network segmentation, and compliance frameworks. Analyze architecture diagrams thoroughly and provide
detailed, actionable security findings in JSON format."""

            response = await self.ollama.generate_with_vision(
                prompt=prompt,
                image_data=image_b64,
                system_prompt=system_prompt
            )

            return response

        except Exception as e:
            logger.error("Vision model call failed", error=str(e))
            raise

    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """
        Parse AI response into structured format
        """
        import json

        try:
            # Extract JSON from response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()

            data = json.loads(response)

            return {
                "components": data.get("components", []),
                "security_assessment": data.get("security_assessment", {
                    "overall": "Analysis completed",
                    "risk_level": "MEDIUM"
                }),
                "weaknesses": data.get("weaknesses", []),
                "zero_trust_proposal": data.get("zero_trust_proposal", {}),
                "secure_by_design": data.get("secure_by_design", {}),
                "compliance": data.get("compliance", {})
            }

        except json.JSONDecodeError as e:
            logger.error("Failed to parse AI response as JSON", error=str(e))
            return {
                "components": [],
                "security_assessment": {
                    "overall": "Analysis completed with limited results",
                    "risk_level": "UNKNOWN"
                },
                "weaknesses": [],
                "zero_trust_proposal": {},
                "secure_by_design": {},
                "compliance": {}
            }
