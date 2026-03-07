from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseMLLM


class OpenAIRealtimeOptions(BaseModel):
    api_key: str = Field(..., description="OpenAI API key")
    model: Optional[str] = Field(default=None, description="Model name (e.g., gpt-4o-realtime-preview)")
    url: Optional[str] = Field(default=None, description="WebSocket URL")
    greeting_message: Optional[str] = Field(default=None, description="Agent greeting message")
    input_modalities: Optional[List[str]] = Field(default=None, description="Input modalities")
    output_modalities: Optional[List[str]] = Field(default=None, description="Output modalities")
    messages: Optional[List[Dict[str, Any]]] = Field(default=None, description="Conversation messages")
    params: Optional[Dict[str, Any]] = Field(default=None, description="Additional parameters")

    class Config:
        extra = "forbid"


class OpenAIRealtime(BaseMLLM):
    def __init__(self, **kwargs: Any):
        self.options = OpenAIRealtimeOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        config: Dict[str, Any] = {
            "vendor": "openai",
            "style": "openai",
            "api_key": self.options.api_key,
        }

        if self.options.url is not None:
            config["url"] = self.options.url
        if self.options.model is not None:
            params = {"model": self.options.model}
            if self.options.params is not None:
                params.update(self.options.params)
            config["params"] = params
        elif self.options.params is not None:
            config["params"] = self.options.params
        if self.options.greeting_message is not None:
            config["greeting_message"] = self.options.greeting_message
        if self.options.input_modalities is not None:
            config["input_modalities"] = self.options.input_modalities
        if self.options.output_modalities is not None:
            config["output_modalities"] = self.options.output_modalities
        if self.options.messages is not None:
            config["messages"] = self.options.messages

        return config


class VertexAIOptions(BaseModel):
    model: str = Field(..., description="Model name")
    project_id: str = Field(..., description="Google Cloud project ID")
    location: str = Field(..., description="Google Cloud location/region")
    adc_credentials_string: str = Field(..., description="Application Default Credentials JSON string")
    instructions: Optional[str] = Field(default=None, description="System instructions")
    voice: Optional[str] = Field(default=None, description="Voice name (e.g., Aoede, Charon)")
    greeting_message: Optional[str] = Field(default=None, description="Agent greeting message")
    input_modalities: Optional[List[str]] = Field(default=None, description="Input modalities")
    output_modalities: Optional[List[str]] = Field(default=None, description="Output modalities")
    messages: Optional[List[Dict[str, Any]]] = Field(default=None, description="Conversation messages")
    additional_params: Optional[Dict[str, Any]] = Field(default=None, description="Additional parameters")

    class Config:
        extra = "forbid"


class VertexAI(BaseMLLM):
    def __init__(self, **kwargs: Any):
        self.options = VertexAIOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "model": self.options.model,
            "project_id": self.options.project_id,
            "location": self.options.location,
            "adc_credentials_string": self.options.adc_credentials_string,
        }

        if self.options.instructions is not None:
            params["instructions"] = self.options.instructions
        if self.options.voice is not None:
            params["voice"] = self.options.voice
        if self.options.additional_params is not None:
            params.update(self.options.additional_params)

        config: Dict[str, Any] = {
            "vendor": "vertexai",
            "style": "openai",
            "params": params,
        }

        if self.options.greeting_message is not None:
            config["greeting_message"] = self.options.greeting_message
        if self.options.input_modalities is not None:
            config["input_modalities"] = self.options.input_modalities
        if self.options.output_modalities is not None:
            config["output_modalities"] = self.options.output_modalities
        if self.options.messages is not None:
            config["messages"] = self.options.messages

        return config
