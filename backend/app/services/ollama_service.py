"""
Ollama Integration Service
Local LLM support using Ollama for free, privacy-focused AI analysis
"""

import httpx
import structlog
from typing import Dict, Any, Optional

logger = structlog.get_logger(__name__)


class OllamaService:
    """
    Service for interacting with Ollama local LLM API
    """

    def __init__(
        self,
        base_url: str = "http://ollama:11434",
        model: str = "llama3.1:8b"
    ):
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient(timeout=300.0)

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4096
    ) -> str:
        """
        Generate text using Ollama

        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        try:
            logger.info(
                "Calling Ollama",
                model=self.model,
                prompt_length=len(prompt)
            )

            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            messages.append({
                "role": "user",
                "content": prompt
            })

            # Call Ollama API
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                }
            )

            response.raise_for_status()
            result = response.json()

            # Extract generated text
            generated_text = result.get("message", {}).get("content", "")

            logger.info(
                "Ollama generation complete",
                response_length=len(generated_text)
            )

            return generated_text

        except httpx.HTTPError as e:
            logger.error("Ollama HTTP error", error=str(e))
            raise Exception(f"Ollama API error: {str(e)}")
        except Exception as e:
            logger.error("Ollama generation failed", error=str(e))
            raise

    async def generate_with_vision(
        self,
        prompt: str,
        image_data: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate text from image using LLaVA model

        Args:
            prompt: Text prompt
            image_data: Base64 encoded image
            system_prompt: System prompt

        Returns:
            Generated analysis
        """
        try:
            logger.info("Calling Ollama vision model")

            # Use LLaVA model for vision tasks
            vision_model = "llava:13b"

            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            messages.append({
                "role": "user",
                "content": prompt,
                "images": [image_data]
            })

            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": vision_model,
                    "messages": messages,
                    "stream": False
                }
            )

            response.raise_for_status()
            result = response.json()

            return result.get("message", {}).get("content", "")

        except Exception as e:
            logger.error("Ollama vision generation failed", error=str(e))
            raise

    async def check_model_availability(self, model_name: str) -> bool:
        """
        Check if a model is available in Ollama

        Args:
            model_name: Name of the model to check

        Returns:
            True if model is available
        """
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()

            models = response.json().get("models", [])
            available_models = [m.get("name") for m in models]

            return model_name in available_models

        except Exception as e:
            logger.error("Failed to check model availability", error=str(e))
            return False

    async def pull_model(self, model_name: str) -> bool:
        """
        Pull a model from Ollama registry

        Args:
            model_name: Model to pull

        Returns:
            True if successful
        """
        try:
            logger.info(f"Pulling model {model_name} from Ollama")

            response = await self.client.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                timeout=600.0  # 10 minutes for large models
            )

            response.raise_for_status()
            logger.info(f"Successfully pulled model {model_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to pull model {model_name}", error=str(e))
            return False

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
