"""Provider-agnostic LLM client. Choose the provider with env vars; tests never change.

LLM_PROVIDER = mock (default) | openai | anthropic | ollama
LLM_MODEL    = optional model override
"""
import os
from typing import Protocol

from src.mock_llm import MockLLM

try:  # optional convenience
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # pragma: no cover
    pass


class LLM(Protocol):
    name: str

    def complete(self, system: str, user: str) -> str: ...


class OpenAILLM:
    def __init__(self, model: str | None = None):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model or "gpt-4o-mini"
        self.name = f"openai:{self.model}"

    def complete(self, system: str, user: str) -> str:
        r = self.client.chat.completions.create(
            model=self.model, temperature=0,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        return r.choices[0].message.content or ""


class AnthropicLLM:
    def __init__(self, model: str | None = None):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = model or "claude-sonnet-5-5"
        self.name = f"anthropic:{self.model}"

    def complete(self, system: str, user: str) -> str:
        r = self.client.messages.create(
            model=self.model, max_tokens=400, temperature=0, system=system,
            messages=[{"role": "user", "content": user}])
        return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")


class OllamaLLM:
    def __init__(self, model: str | None = None):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model or "llama3.1"
        self.name = f"ollama:{self.model}"

    def complete(self, system: str, user: str) -> str:
        import requests
        r = requests.post(f"{self.host}/api/chat", timeout=120, json={
            "model": self.model, "stream": False, "options": {"temperature": 0},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]})
        r.raise_for_status()
        return r.json()["message"]["content"]


def provider_name() -> str:
    return os.getenv("LLM_PROVIDER", "mock").lower()


def get_llm() -> LLM:
    provider, model = provider_name(), os.getenv("LLM_MODEL") or None
    if provider == "mock":
        return MockLLM()
    if provider == "openai":
        return OpenAILLM(model)
    if provider == "anthropic":
        return AnthropicLLM(model)
    if provider == "ollama":
        return OllamaLLM(model)
    raise ValueError(f"Unknown LLM_PROVIDER '{provider}'")
