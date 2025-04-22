"""
LLM Config Module.

This module defines the `LLMConfig` TypedDict, which represents the configuration
for Language Model (LLM) providers. It ensures type safety and clarity when passing
LLM-related parameters to the agent.
"""

# Standard library imports
from typing import Optional

# Third-party imports
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """
    TypedDict for Language Model (LLM) configuration.

    Attributes:
        provider (str): The name of the LLM provider (e.g., "OpenAI").
        model (Optional[str]): The specific model to use (e.g., "gpt-4").
            Defaults to the provider's default model if not provided.
        temperature (Optional[str]): The model temperature parameter.
        provider_api_key (str): The API key for the provider. This field is mandatory.

    Example:
        >>> from lib.types.llm_config import LLMConfig
        >>> llm_config: LLMConfig = {
        ...     "provider": "OpenAI",
        ...     "model": "gpt-4o-mini",
        ...     "temperature": 0,
        ...     "provider_api_key": "your-api-key"
        ... }
    """

    provider: Optional[str] = Field(default="OpenAI")
    model: Optional[str] = Field(default="gpt-4o-mini")
    temperature: Optional[float] = Field(default=0.7)
    provider_api_key: str = Field(alias="provider-api-key")
