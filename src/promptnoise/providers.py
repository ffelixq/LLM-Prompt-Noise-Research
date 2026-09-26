from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

load_dotenv()


@dataclass
class ProviderResult:
    text: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    reasoning_tokens: int | None = None
    cached_tokens: int | None = None
    raw_usage: dict[str, Any] | None = None


def _attr(obj: Any, path: str, default=None):
    current = obj
    for part in path.split("."):
        if current is None:
            return default
        if isinstance(current, dict):
            current = current.get(part)
        else:
            current = getattr(current, part, None)
    return default if current is None else current


class BaseProvider:
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.model = config["model"]

    def generate(self, prompt: str) -> ProviderResult:
        raise NotImplementedError


class OpenAIProvider(BaseProvider):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        from openai import OpenAI

        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def generate(self, prompt: str) -> ProviderResult:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "input": prompt,
            "max_output_tokens": int(self.config.get("max_output_tokens", 128)),
        }
        if self.config.get("temperature") is not None:
            kwargs["temperature"] = self.config["temperature"]
        if self.config.get("reasoning_effort"):
            kwargs["reasoning"] = {"effort": self.config["reasoning_effort"]}

        response = self.client.responses.create(**kwargs)
        usage = response.usage
        return ProviderResult(
            text=response.output_text or "",
            input_tokens=_attr(usage, "input_tokens"),
            output_tokens=_attr(usage, "output_tokens"),
            reasoning_tokens=_attr(usage, "output_tokens_details.reasoning_tokens"),
            cached_tokens=_attr(usage, "input_tokens_details.cached_tokens"),
            raw_usage=usage.model_dump() if hasattr(usage, "model_dump") else None,
        )


class GroqProvider(BaseProvider):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        from groq import Groq

        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def generate(self, prompt: str) -> ProviderResult:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": int(self.config.get("max_output_tokens", 128)),
        }
        if self.config.get("temperature") is not None:
            kwargs["temperature"] = self.config["temperature"]
        if self.config.get("reasoning_effort"):
            kwargs["reasoning_effort"] = self.config["reasoning_effort"]

        response = self.client.chat.completions.create(**kwargs)
        usage = response.usage
        text = response.choices[0].message.content or ""
        return ProviderResult(
            text=text,
            input_tokens=_attr(usage, "prompt_tokens"),
            output_tokens=_attr(usage, "completion_tokens"),
            reasoning_tokens=_attr(usage, "completion_tokens_details.reasoning_tokens"),
            cached_tokens=_attr(usage, "prompt_tokens_details.cached_tokens"),
            raw_usage=usage.model_dump() if hasattr(usage, "model_dump") else None,
        )


class AnthropicProvider(BaseProvider):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        from anthropic import Anthropic

        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def generate(self, prompt: str) -> ProviderResult:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": int(self.config.get("max_output_tokens", 128)),
            "messages": [{"role": "user", "content": prompt}],
        }
        if self.config.get("temperature") is not None:
            kwargs["temperature"] = self.config["temperature"]

        response = self.client.messages.create(**kwargs)
        text = "".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        )
        usage = response.usage
        return ProviderResult(
            text=text,
            input_tokens=_attr(usage, "input_tokens"),
            output_tokens=_attr(usage, "output_tokens"),
            raw_usage=usage.model_dump() if hasattr(usage, "model_dump") else None,
        )


class GoogleProvider(BaseProvider):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        from google import genai

        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    def generate(self, prompt: str) -> ProviderResult:
        from google.genai import types

        config_kwargs: dict[str, Any] = {
            "max_output_tokens": int(self.config.get("max_output_tokens", 128)),
        }
        if self.config.get("temperature") is not None:
            config_kwargs["temperature"] = self.config["temperature"]

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        usage = response.usage_metadata
        return ProviderResult(
            text=response.text or "",
            input_tokens=_attr(usage, "prompt_token_count"),
            output_tokens=_attr(usage, "candidates_token_count"),
            reasoning_tokens=_attr(usage, "thoughts_token_count"),
            cached_tokens=_attr(usage, "cached_content_token_count"),
            raw_usage=usage.model_dump() if hasattr(usage, "model_dump") else None,
        )


class DeepSeekProvider(BaseProvider):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        from openai import OpenAI

        self.client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url=self.config.get("base_url", "https://api.deepseek.com"),
        )

    def generate(self, prompt: str) -> ProviderResult:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": int(self.config.get("max_output_tokens", 128)),
        }
        if self.config.get("temperature") is not None:
            kwargs["temperature"] = self.config["temperature"]

        response = self.client.chat.completions.create(**kwargs)
        usage = response.usage
        text = response.choices[0].message.content or ""
        return ProviderResult(
            text=text,
            input_tokens=_attr(usage, "prompt_tokens"),
            output_tokens=_attr(usage, "completion_tokens"),
            reasoning_tokens=_attr(usage, "completion_tokens_details.reasoning_tokens"),
            cached_tokens=_attr(usage, "prompt_tokens_details.cached_tokens"),
            raw_usage=usage.model_dump() if hasattr(usage, "model_dump") else None,
        )


def make_provider(config: dict[str, Any]) -> BaseProvider:
    provider = str(config["provider"]).lower()
    mapping = {
        "openai": OpenAIProvider,
        "groq": GroqProvider,
        "anthropic": AnthropicProvider,
        "google": GoogleProvider,
        "deepseek": DeepSeekProvider,
    }
    if provider not in mapping:
        raise ValueError(f"Unsupported provider: {provider}")
    return mapping[provider](config)
