from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OpenAISettings:
    api_key: str
    model: str = "gpt-5.2"
    temperature: float = 0.4
    max_output_tokens: int = 800
    timeout_seconds: int = 60
    base_url: str = "https://api.openai.com/v1/responses"
