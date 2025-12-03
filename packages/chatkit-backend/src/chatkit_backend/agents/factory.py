"""
LLM provider factory for creating model instances.

Supports:
- OpenAI (default)
- Gemini via OpenAI-compatible API

Environment variables:
- LLM_PROVIDER: "openai" or "gemini" (default: "openai")
- OPENAI_API_KEY: OpenAI API key
- GEMINI_API_KEY: Gemini API key
- OPENAI_DEFAULT_MODEL: Model name for OpenAI (default: "gpt-4o-mini")
- GEMINI_DEFAULT_MODEL: Model name for Gemini (default: "gemini-2.5-flash")
"""

import os
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel


def create_model() -> OpenAIChatCompletionsModel:
    """
    Create an LLM model instance based on environment configuration.

    Returns:
        OpenAIChatCompletionsModel configured for the selected provider

    Raises:
        ValueError: If provider is unsupported or API key is missing
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required when LLM_PROVIDER=gemini"
            )

        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        model_name = os.getenv("GEMINI_DEFAULT_MODEL", "gemini-2.5-flash")

        return OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=client
        )

    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required when LLM_PROVIDER=openai"
            )

        client = AsyncOpenAI(api_key=api_key)
        model_name = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")

        return OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=client
        )

    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider}. "
            f"Supported providers: openai, gemini"
        )
