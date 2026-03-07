from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from .base import BaseSTT


class SpeechmaticsSTTOptions(BaseModel):
    api_key: str = Field(..., description="Speechmatics API key")
    language: str = Field(..., description="Language code (e.g., en, es, fr)")
    additional_params: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        extra = "forbid"


class SpeechmaticsSTT(BaseSTT):
    def __init__(self, **kwargs: Any):
        self.options = SpeechmaticsSTTOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "api_key": self.options.api_key,
            "language": self.options.language,
        }
        if self.options.additional_params is not None:
            params.update(self.options.additional_params)

        return {
            "vendor": "speechmatics",
            "language": self.options.language,
            "params": params,
        }


class DeepgramSTTOptions(BaseModel):
    api_key: Optional[str] = Field(default=None, description="Deepgram API key")
    model: Optional[str] = Field(default=None, description="Model (e.g., nova-2, enhanced, base)")
    language: Optional[str] = Field(default=None, description="Language code (e.g., en-US)")
    smart_format: Optional[bool] = Field(default=None, description="Enable smart formatting")
    punctuation: Optional[bool] = Field(default=None, description="Enable punctuation")
    additional_params: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        extra = "forbid"


class DeepgramSTT(BaseSTT):
    def __init__(self, **kwargs: Any):
        self.options = DeepgramSTTOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {}

        if self.options.api_key is not None:
            params["api_key"] = self.options.api_key
        if self.options.model is not None:
            params["model"] = self.options.model
        if self.options.language is not None:
            params["language"] = self.options.language
        if self.options.smart_format is not None:
            params["smart_format"] = self.options.smart_format
        if self.options.punctuation is not None:
            params["punctuation"] = self.options.punctuation
        if self.options.additional_params is not None:
            params.update(self.options.additional_params)

        return {
            "vendor": "deepgram",
            "language": self.options.language,
            "params": params,
        }


class MicrosoftSTTOptions(BaseModel):
    key: str = Field(..., description="Azure subscription key")
    region: str = Field(..., description="Azure region (e.g., eastus)")
    language: Optional[str] = Field(default=None, description="Language code (e.g., en-US)")
    additional_params: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        extra = "forbid"


class MicrosoftSTT(BaseSTT):
    def __init__(self, **kwargs: Any):
        self.options = MicrosoftSTTOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "key": self.options.key,
            "region": self.options.region,
        }
        if self.options.language is not None:
            params["language"] = self.options.language
        if self.options.additional_params is not None:
            params.update(self.options.additional_params)

        return {
            "vendor": "microsoft",
            "language": self.options.language,
            "params": params,
        }


class OpenAISTTOptions(BaseModel):
    api_key: str = Field(..., description="OpenAI API key")
    model: Optional[str] = Field(default=None, description="Model (default: whisper-1)")
    language: Optional[str] = Field(default=None, description="Language code")
    additional_params: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        extra = "forbid"


class OpenAISTT(BaseSTT):
    def __init__(self, **kwargs: Any):
        self.options = OpenAISTTOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"api_key": self.options.api_key}

        if self.options.model is not None:
            params["model"] = self.options.model
        if self.options.additional_params is not None:
            params.update(self.options.additional_params)

        return {
            "vendor": "openai",
            "language": self.options.language,
            "params": params,
        }


class GoogleSTTOptions(BaseModel):
    api_key: str = Field(..., description="Google Cloud API key")
    language: Optional[str] = Field(default=None, description="Language code (e.g., en-US)")
    additional_params: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        extra = "forbid"


class GoogleSTT(BaseSTT):
    def __init__(self, **kwargs: Any):
        self.options = GoogleSTTOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"api_key": self.options.api_key}

        if self.options.language is not None:
            params["language"] = self.options.language
        if self.options.additional_params is not None:
            params.update(self.options.additional_params)

        return {
            "vendor": "google",
            "language": self.options.language,
            "params": params,
        }


class AmazonSTTOptions(BaseModel):
    access_key: str = Field(..., description="AWS Access Key ID")
    secret_key: str = Field(..., description="AWS Secret Access Key")
    region: str = Field(..., description="AWS region (e.g., us-east-1)")
    language: Optional[str] = Field(default=None, description="Language code")
    additional_params: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        extra = "forbid"


class AmazonSTT(BaseSTT):
    def __init__(self, **kwargs: Any):
        self.options = AmazonSTTOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "access_key": self.options.access_key,
            "secret_key": self.options.secret_key,
            "region": self.options.region,
        }
        if self.options.language is not None:
            params["language"] = self.options.language
        if self.options.additional_params is not None:
            params.update(self.options.additional_params)

        return {
            "vendor": "amazon",
            "language": self.options.language,
            "params": params,
        }


class AssemblyAISTTOptions(BaseModel):
    api_key: str = Field(..., description="AssemblyAI API key")
    language: Optional[str] = Field(default=None, description="Language code")
    additional_params: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        extra = "forbid"


class AssemblyAISTT(BaseSTT):
    def __init__(self, **kwargs: Any):
        self.options = AssemblyAISTTOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"api_key": self.options.api_key}
        if self.options.additional_params is not None:
            params.update(self.options.additional_params)

        return {
            "vendor": "assemblyai",
            "language": self.options.language,
            "params": params,
        }


class AresSTTOptions(BaseModel):
    language: Optional[str] = Field(default=None, description="Language code")
    additional_params: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        extra = "forbid"


class AresSTT(BaseSTT):
    def __init__(self, **kwargs: Any):
        self.options = AresSTTOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if self.options.language is not None:
            params["language"] = self.options.language
        if self.options.additional_params is not None:
            params.update(self.options.additional_params)

        return {
            "vendor": "ares",
            "language": self.options.language,
            "params": params,
        }


class SarvamSTTOptions(BaseModel):
    api_key: str = Field(..., description="Sarvam API key")
    language: str = Field(..., description="Language code (e.g., en, hi, ta)")
    additional_params: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        extra = "forbid"


class SarvamSTT(BaseSTT):
    def __init__(self, **kwargs: Any):
        self.options = SarvamSTTOptions(**kwargs)

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "api_key": self.options.api_key,
            "language": self.options.language,
        }
        if self.options.additional_params is not None:
            params.update(self.options.additional_params)

        return {
            "vendor": "sarvam",
            "language": self.options.language,
            "params": params,
        }
