from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseTTS, CartesiaSampleRate, ElevenLabsSampleRate, MicrosoftSampleRate


class ElevenLabsTTSOptions(BaseModel):
    key: str = Field(..., description="ElevenLabs API key")
    model_id: str = Field(..., description="Model ID (e.g., eleven_flash_v2_5)")
    voice_id: str = Field(..., description="Voice ID")
    base_url: Optional[str] = Field(default=None, description="WebSocket base URL")
    sample_rate: Optional[ElevenLabsSampleRate] = Field(default=None, description="Sample rate in Hz")
    skip_patterns: Optional[List[int]] = Field(default=None)
    optimize_streaming_latency: Optional[int] = Field(default=None, ge=0, le=4)
    stability: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    similarity_boost: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    style: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    use_speaker_boost: Optional[bool] = Field(default=None)

    class Config:
        extra = "forbid"


class ElevenLabsTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = ElevenLabsTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return self.options.sample_rate

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "key": self.options.key,
            "model_id": self.options.model_id,
            "voice_id": self.options.voice_id,
        }

        if self.options.base_url is not None:
            params["base_url"] = self.options.base_url
        if self.options.sample_rate is not None:
            params["sample_rate"] = self.options.sample_rate
        if self.options.optimize_streaming_latency is not None:
            params["optimize_streaming_latency"] = self.options.optimize_streaming_latency
        if self.options.stability is not None:
            params["stability"] = self.options.stability
        if self.options.similarity_boost is not None:
            params["similarity_boost"] = self.options.similarity_boost
        if self.options.style is not None:
            params["style"] = self.options.style
        if self.options.use_speaker_boost is not None:
            params["use_speaker_boost"] = self.options.use_speaker_boost

        result: Dict[str, Any] = {"vendor": "elevenlabs", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class MicrosoftTTSOptions(BaseModel):
    key: str = Field(..., description="Azure subscription key")
    region: str = Field(..., description="Azure region (e.g., eastus)")
    voice_name: str = Field(..., description="Voice name")
    sample_rate: Optional[MicrosoftSampleRate] = Field(default=None, description="Sample rate in Hz")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class MicrosoftTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = MicrosoftTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return self.options.sample_rate

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "key": self.options.key,
            "region": self.options.region,
            "voice_name": self.options.voice_name,
        }

        if self.options.sample_rate is not None:
            params["sample_rate"] = self.options.sample_rate

        result: Dict[str, Any] = {"vendor": "microsoft", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class OpenAITTSOptions(BaseModel):
    key: str = Field(..., description="OpenAI API key")
    voice: str = Field(..., description="Voice name (alloy, echo, fable, onyx, nova, shimmer)")
    model: Optional[str] = Field(default=None, description="Model name (tts-1, tts-1-hd)")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class OpenAITTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = OpenAITTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return 24000

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "key": self.options.key,
            "voice": self.options.voice,
        }

        if self.options.model is not None:
            params["model"] = self.options.model

        result: Dict[str, Any] = {"vendor": "openai", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class CartesiaTTSOptions(BaseModel):
    key: str = Field(..., description="Cartesia API key")
    voice_id: str = Field(..., description="Voice ID")
    model_id: Optional[str] = Field(default=None, description="Model ID")
    sample_rate: Optional[CartesiaSampleRate] = Field(default=None, description="Sample rate in Hz")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class CartesiaTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = CartesiaTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return self.options.sample_rate

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "key": self.options.key,
            "voice_id": self.options.voice_id,
        }

        if self.options.model_id is not None:
            params["model_id"] = self.options.model_id
        if self.options.sample_rate is not None:
            params["sample_rate"] = self.options.sample_rate

        result: Dict[str, Any] = {"vendor": "cartesia", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class GoogleTTSOptions(BaseModel):
    key: str = Field(..., description="Google Cloud API key")
    voice_name: str = Field(..., description="Voice name")
    language_code: Optional[str] = Field(default=None, description="Language code (e.g., en-US)")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class GoogleTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = GoogleTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return None

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "key": self.options.key,
            "voice_name": self.options.voice_name,
        }

        if self.options.language_code is not None:
            params["language_code"] = self.options.language_code

        result: Dict[str, Any] = {"vendor": "google", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class AmazonTTSOptions(BaseModel):
    access_key: str = Field(..., description="AWS access key")
    secret_key: str = Field(..., description="AWS secret key")
    region: str = Field(..., description="AWS region (e.g., us-east-1)")
    voice_id: str = Field(..., description="Amazon Polly voice ID")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class AmazonTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = AmazonTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return None

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "access_key": self.options.access_key,
            "secret_key": self.options.secret_key,
            "region": self.options.region,
            "voice_id": self.options.voice_id,
        }

        result: Dict[str, Any] = {"vendor": "amazon", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class HumeAITTSOptions(BaseModel):
    key: str = Field(..., description="Hume AI API key")
    config_id: Optional[str] = Field(default=None, description="Configuration ID")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class HumeAITTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = HumeAITTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return None

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"key": self.options.key}

        if self.options.config_id is not None:
            params["config_id"] = self.options.config_id

        result: Dict[str, Any] = {"vendor": "humeai", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class RimeTTSOptions(BaseModel):
    key: str = Field(..., description="Rime API key")
    speaker: str = Field(..., description="Speaker ID")
    model_id: Optional[str] = Field(default=None, description="Model ID")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class RimeTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = RimeTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return None

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "key": self.options.key,
            "speaker": self.options.speaker,
        }

        if self.options.model_id is not None:
            params["model_id"] = self.options.model_id

        result: Dict[str, Any] = {"vendor": "rime", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class FishAudioTTSOptions(BaseModel):
    key: str = Field(..., description="Fish Audio API key")
    reference_id: str = Field(..., description="Reference ID")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class FishAudioTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = FishAudioTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return None

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "key": self.options.key,
            "reference_id": self.options.reference_id,
        }

        result: Dict[str, Any] = {"vendor": "fishaudio", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class MiniMaxTTSOptions(BaseModel):
    key: str = Field(..., description="MiniMax API key")
    voice_id: Optional[str] = Field(default=None, description="Voice ID")
    model: Optional[str] = Field(default=None, description="Model name")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class MiniMaxTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = MiniMaxTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return None

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"key": self.options.key}

        if self.options.voice_id is not None:
            params["voice_id"] = self.options.voice_id
        if self.options.model is not None:
            params["model"] = self.options.model

        result: Dict[str, Any] = {"vendor": "minimax", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class SarvamTTSOptions(BaseModel):
    api_key: str = Field(..., description="Sarvam API key")
    voice_id: Optional[str] = Field(default=None, description="Voice ID")
    model: Optional[str] = Field(default=None, description="Model name")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class SarvamTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = SarvamTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return None

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"api_key": self.options.api_key}

        if self.options.voice_id is not None:
            params["voice_id"] = self.options.voice_id
        if self.options.model is not None:
            params["model"] = self.options.model

        result: Dict[str, Any] = {"vendor": "sarvam", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result
