from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseLLM


class OpenAIOptions(BaseModel):
    api_key: str = Field(..., description="OpenAI API key")
    model: str = Field(default="gpt-4o-mini", description="Model name")
    base_url: Optional[str] = Field(default=None, description="Custom base URL")
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(default=None, gt=0)
    system_messages: Optional[List[Dict[str, Any]]] = Field(default=None)
    greeting_message: Optional[str] = Field(default=None)
    failure_message: Optional[str] = Field(default=None)
    input_modalities: Optional[List[str]] = Field(default=None)
    params: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        extra = "forbid"


class OpenAI(BaseLLM):
    def __init__(self, **kwargs: Any):
        self.options = OpenAIOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        # model is the default; explicit params entries extend/override it.
        # This matches the TS SDK behaviour: { model, ...params }.
        params: Dict[str, Any] = {"model": self.options.model, **(self.options.params or {})}

        # Named fields take precedence over anything in the generic params dict.
        if self.options.max_tokens is not None:
            params["max_tokens"] = self.options.max_tokens
        if self.options.temperature is not None:
            params["temperature"] = self.options.temperature
        if self.options.top_p is not None:
            params["top_p"] = self.options.top_p

        config: Dict[str, Any] = {
            "url": self.options.base_url or "https://api.openai.com/v1/chat/completions",
            "api_key": self.options.api_key,
            "params": params,
            "style": "openai",
            "input_modalities": self.options.input_modalities or ["text"],
        }

        if self.options.system_messages is not None:
            config["system_messages"] = self.options.system_messages
        if self.options.greeting_message is not None:
            config["greeting_message"] = self.options.greeting_message
        if self.options.failure_message is not None:
            config["failure_message"] = self.options.failure_message

        return config


class AzureOpenAIOptions(BaseModel):
    api_key: str = Field(..., description="Azure OpenAI API key")
    endpoint: str = Field(..., description="Azure endpoint URL")
    deployment_name: str = Field(..., description="Azure deployment name")
    api_version: str = Field(default="2024-08-01-preview", description="Azure API version")
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(default=None, gt=0)
    system_messages: Optional[List[Dict[str, Any]]] = Field(default=None)
    greeting_message: Optional[str] = Field(default=None)
    failure_message: Optional[str] = Field(default=None)
    input_modalities: Optional[List[str]] = Field(default=None)

    class Config:
        extra = "forbid"


class AzureOpenAI(BaseLLM):
    def __init__(self, **kwargs: Any):
        self.options = AzureOpenAIOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        url = (
            f"{self.options.endpoint}/openai/deployments/"
            f"{self.options.deployment_name}/chat/completions"
            f"?api-version={self.options.api_version}"
        )
        config: Dict[str, Any] = {
            "url": url,
            "api_key": self.options.api_key,
            "vendor": "azure",
            "style": "openai",
            "input_modalities": self.options.input_modalities or ["text"],
        }

        params: Dict[str, Any] = {}
        if self.options.temperature is not None:
            params["temperature"] = self.options.temperature
        if self.options.top_p is not None:
            params["top_p"] = self.options.top_p
        if self.options.max_tokens is not None:
            params["max_tokens"] = self.options.max_tokens
        if params:
            config["params"] = params

        if self.options.system_messages is not None:
            config["system_messages"] = self.options.system_messages
        if self.options.greeting_message is not None:
            config["greeting_message"] = self.options.greeting_message
        if self.options.failure_message is not None:
            config["failure_message"] = self.options.failure_message

        return config


class AnthropicOptions(BaseModel):
    api_key: str = Field(..., description="Anthropic API key")
    model: str = Field(default="claude-3-5-sonnet-20241022", description="Model name")
    max_tokens: Optional[int] = Field(default=None, gt=0)
    temperature: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    top_p: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    system_messages: Optional[List[Dict[str, Any]]] = Field(default=None)
    greeting_message: Optional[str] = Field(default=None)
    failure_message: Optional[str] = Field(default=None)
    input_modalities: Optional[List[str]] = Field(default=None)

    class Config:
        extra = "forbid"


class Anthropic(BaseLLM):
    def __init__(self, **kwargs: Any):
        self.options = AnthropicOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        config: Dict[str, Any] = {
            "url": "https://api.anthropic.com/v1/messages",
            "api_key": self.options.api_key,
            "params": {"model": self.options.model},
            "style": "anthropic",
            "input_modalities": self.options.input_modalities or ["text"],
        }

        if self.options.max_tokens is not None:
            config["params"]["max_tokens"] = self.options.max_tokens
        if self.options.temperature is not None:
            config["params"]["temperature"] = self.options.temperature
        if self.options.top_p is not None:
            config["params"]["top_p"] = self.options.top_p
        if self.options.system_messages is not None:
            config["system_messages"] = self.options.system_messages
        if self.options.greeting_message is not None:
            config["greeting_message"] = self.options.greeting_message
        if self.options.failure_message is not None:
            config["failure_message"] = self.options.failure_message

        return config


class GeminiOptions(BaseModel):
    api_key: str = Field(..., description="Google AI API key")
    model: str = Field(default="gemini-2.0-flash-exp", description="Model name")
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    top_k: Optional[int] = Field(default=None, gt=0)
    max_output_tokens: Optional[int] = Field(default=None, gt=0)
    system_messages: Optional[List[Dict[str, Any]]] = Field(default=None)
    greeting_message: Optional[str] = Field(default=None)
    failure_message: Optional[str] = Field(default=None)
    input_modalities: Optional[List[str]] = Field(default=None)

    class Config:
        extra = "forbid"


class Gemini(BaseLLM):
    def __init__(self, **kwargs: Any):
        self.options = GeminiOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        config: Dict[str, Any] = {
            "url": "https://generativelanguage.googleapis.com/v1beta/models",
            "api_key": self.options.api_key,
            "params": {"model": self.options.model},
            "style": "gemini",
            "input_modalities": self.options.input_modalities or ["text"],
        }

        if self.options.temperature is not None:
            config["params"]["temperature"] = self.options.temperature
        if self.options.top_p is not None:
            config["params"]["top_p"] = self.options.top_p
        if self.options.top_k is not None:
            config["params"]["top_k"] = self.options.top_k
        if self.options.max_output_tokens is not None:
            config["params"]["max_output_tokens"] = self.options.max_output_tokens
        if self.options.system_messages is not None:
            config["system_messages"] = self.options.system_messages
        if self.options.greeting_message is not None:
            config["greeting_message"] = self.options.greeting_message
        if self.options.failure_message is not None:
            config["failure_message"] = self.options.failure_message

        return config
