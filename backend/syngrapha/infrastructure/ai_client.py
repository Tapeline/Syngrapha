import json
from typing import Final

from aiohttp import ClientSession

from syngrapha.config import AIConfig

_URL: Final = "https://openrouter.ai/api/v1/chat/completions"
_MODEL: Final = "meta-llama/llama-3.3-70b-instruct:free"


class AIClientError(ValueError):
    """Raised when AI answers badly."""


class OpenRouterAI:
    """AI client."""

    def __init__(self, config: AIConfig) -> None:
        """Create client."""
        self.key = config.key

    async def request(self, prompt: str) -> str:
        async with (
            ClientSession() as session,
            session.post(
                _URL,
                headers={
                    "Authorization": f"Bearer {self.key}",
                    "Accept": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3.3-70b-instruct:free",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            ) as response
        ):
            if response.status != 200:
                raise AIClientError
            data = await response.json()
            return data["choices"][0]["message"]["content"]


class GeminiAI:
    """Gemini AI client."""

    def __init__(self, config: AIConfig) -> None:
        """Create client."""
        self.key = config.key

    async def request(self, prompt: str) -> str:
        async with (
            ClientSession() as session,
            session.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
                headers={
                    "X-goog-api-key": self.key,
                    "Content-Type": "application/json"
                },
                json={"contents": [{"parts": [{"text": prompt}]}]}
            ) as response
        ):
            if response.status != 200:
                raise AIClientError
            data = await response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
