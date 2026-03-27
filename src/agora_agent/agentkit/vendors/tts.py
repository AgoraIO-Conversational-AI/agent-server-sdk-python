from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseTTS, CartesiaSampleRate, ElevenLabsSampleRate, GoogleTTSSampleRate, MicrosoftSampleRate


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
    api_key: str = Field(..., description="OpenAI API key")
    voice: str = Field(..., description="Voice name (alloy, echo, fable, onyx, nova, shimmer)")
    model: Optional[str] = Field(default=None, description="Model name (tts-1, tts-1-hd)")
    response_format: Optional[str] = Field(default=None, description="Audio format (e.g., pcm)")
    speed: Optional[float] = Field(default=None, description="Speech speed multiplier")
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
            "api_key": self.options.api_key,
            "voice": self.options.voice,
        }

        if self.options.model is not None:
            params["model"] = self.options.model
        if self.options.response_format is not None:
            params["response_format"] = self.options.response_format
        if self.options.speed is not None:
            params["speed"] = self.options.speed

        result: Dict[str, Any] = {"vendor": "openai", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class CartesiaTTSOptions(BaseModel):
    api_key: str = Field(..., description="Cartesia API key")
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
            "api_key": self.options.api_key,
            "voice": {"mode": "id", "id": self.options.voice_id},
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
    sample_rate_hertz: Optional[GoogleTTSSampleRate] = Field(default=None, description="Sample rate in Hz")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class GoogleTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = GoogleTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return self.options.sample_rate_hertz

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "key": self.options.key,
            "voice_name": self.options.voice_name,
        }

        if self.options.language_code is not None:
            params["language_code"] = self.options.language_code
        if self.options.sample_rate_hertz is not None:
            params["sample_rate_hertz"] = self.options.sample_rate_hertz

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
    lang: Optional[str] = Field(default=None, description="Language code")
    sampling_rate: Optional[int] = Field(default=None, description="Sampling rate in Hz")
    speed_alpha: Optional[float] = Field(default=None, description="Speed multiplier")
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
        if self.options.lang is not None:
            params["lang"] = self.options.lang
        if self.options.sampling_rate is not None:
            params["samplingRate"] = self.options.sampling_rate
        if self.options.speed_alpha is not None:
            params["speedAlpha"] = self.options.speed_alpha

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
    group_id: str = Field(..., description="MiniMax group identifier")
    model: str = Field(..., description="TTS model (e.g., 'speech-02-turbo')")
    voice_id: str = Field(..., description="Voice style identifier (e.g., 'English_captivating_female1')")
    url: str = Field(..., description="WebSocket endpoint (e.g., 'wss://api-uw.minimax.io/ws/v1/t2a_v2')")
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
        params: Dict[str, Any] = {
            "key": self.options.key,
            "group_id": self.options.group_id,
            "model": self.options.model,
            "voice_setting": {"voice_id": self.options.voice_id},
            "url": self.options.url,
        }

        result: Dict[str, Any] = {"vendor": "minimax", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class SarvamTTSOptions(BaseModel):
    key: str = Field(..., description="Sarvam API subscription key")
    speaker: str = Field(..., description="Speaker/voice ID (e.g., 'anushka', 'abhilash', 'karun', 'hitesh', 'manisha', 'vidya', 'arya')")
    target_language_code: str = Field(..., description="Target language code (e.g., 'en-IN', 'hi-IN', 'ta-IN')")
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
        params: Dict[str, Any] = {
            "key": self.options.key,
            "speaker": self.options.speaker,
            "target_language_code": self.options.target_language_code,
        }

        result: Dict[str, Any] = {"vendor": "sarvam", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result


class MurfTTSOptions(BaseModel):
    key: str = Field(..., description="Murf API key")
    voice_id: str = Field(..., description="Voice ID (e.g., 'Ariana', 'Natalie', 'Ken')")
    style: Optional[str] = Field(default=None, description="Voice style (e.g., 'Angry', 'Sad', 'Conversational', 'Newscast')")
    skip_patterns: Optional[List[int]] = Field(default=None)

    class Config:
        extra = "forbid"


class MurfTTS(BaseTTS):
    def __init__(self, **kwargs: Any):
        self.options = MurfTTSOptions(**kwargs)

    @property
    def sample_rate(self) -> Optional[int]:
        return None

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "key": self.options.key,
            "voice_id": self.options.voice_id,
        }

        if self.options.style is not None:
            params["style"] = self.options.style

        result: Dict[str, Any] = {"vendor": "murf", "params": params}
        if self.options.skip_patterns is not None:
            result["skip_patterns"] = self.options.skip_patterns
        return result
