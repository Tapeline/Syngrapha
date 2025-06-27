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
            breakpoint()
            if response.status != 200:
                raise AIClientError
            data = await response.json()
            return data["choices"][0]["message"]["content"]
