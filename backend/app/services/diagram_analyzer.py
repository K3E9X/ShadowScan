"""
Diagram Analyzer Service
AI-powered architecture diagram analysis using vision models
"""

import uuid
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
import structlog
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from app.core.config import settings
from app.services.prompts import DIAGRAM_ANALYSIS_PROMPT

logger = structlog.get_logger(__name__)


class DiagramAnalyzerService:
    """
    Service for analyzing architecture diagrams using AI vision models
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
        file_content: bytes,
        filename: str,
        content_type: str
    ) -> Dict[str, Any]:
        """
        Perform security analysis on architecture diagram

        Args:
            file_content: Image file bytes
            filename: Original filename
            content_type: MIME type

        Returns:
            Analysis results with components, weaknesses, and recommendations
        """
        try:
            logger.info(
                "Starting diagram analysis",
                filename=filename,
                content_type=content_type
            )

            # Generate analysis ID
            analysis_id = str(uuid.uuid4())

            # Convert image to base64 for vision API
            image_b64 = base64.b64encode(file_content).decode('utf-8')

            # Build prompt
            prompt = DIAGRAM_ANALYSIS_PROMPT

            # Call AI vision model
            ai_response = await self._call_vision_model(prompt, image_b64, content_type)

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
                    "analyzer_version": "1.0.0"
                }
            })

            return results

        except Exception as e:
            logger.error("Diagram analysis failed", error=str(e), exc_info=True)
            raise

    async def _call_vision_model(
        self,
        prompt: str,
        image_b64: str,
        content_type: str
    ) -> str:
        """
        Call AI vision model (Claude Vision or GPT-4 Vision)
        """
        try:
            if self.anthropic_client:
                logger.debug("Using Claude Vision for analysis")

                # Map content type to media type
                media_type_map = {
                    "image/png": "image/png",
                    "image/jpeg": "image/jpeg",
                    "image/jpg": "image/jpeg",
                    "image/svg+xml": "image/png"  # Convert SVG to PNG first
                }

                media_type = media_type_map.get(content_type, "image/png")

                response = await self.anthropic_client.messages.create(
                    model=settings.AI_MODEL_VISION,
                    max_tokens=settings.AI_MAX_TOKENS,
                    temperature=settings.AI_TEMPERATURE,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": media_type,
                                        "data": image_b64
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                )
                return response.content[0].text

            elif self.openai_client:
                logger.debug("Using GPT-4 Vision for analysis")

                response = await self.openai_client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{content_type};base64,{image_b64}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=settings.AI_MAX_TOKENS,
                    temperature=settings.AI_TEMPERATURE
                )
                return response.choices[0].message.content

            else:
                raise ValueError("No AI API key configured")

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
