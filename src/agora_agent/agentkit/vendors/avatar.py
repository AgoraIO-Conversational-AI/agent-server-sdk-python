from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .base import BaseAvatar

HEYGEN_SAMPLE_RATE = 24000
LIVEAVATAR_SAMPLE_RATE = 24000
AKOOL_SAMPLE_RATE = 16000


class HeyGenAvatarOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key: str = Field(..., description="HeyGen API key")
    quality: str = Field(..., description="Avatar quality: low, medium, or high")
    agora_uid: str = Field(..., description="Agora UID for the avatar stream")
    agora_token: Optional[str] = Field(default=None, description="RTC token for avatar authentication")
    avatar_id: Optional[str] = Field(default=None, description="HeyGen avatar ID")
    enable: Optional[bool] = Field(default=None, description="Enable avatar (default: true)")
    disable_idle_timeout: Optional[bool] = Field(default=None, description="Whether to disable idle timeout")
    activity_idle_timeout: Optional[int] = Field(default=None, description="Idle timeout in seconds")
    additional_params: Optional[Dict[str, Any]] = Field(default=None, description="Additional vendor-specific parameters")

    @field_validator("quality")
    @classmethod
    def validate_quality(cls, v: str) -> str:
        valid = ("low", "medium", "high")
        if v not in valid:
            raise ValueError(f"Invalid quality '{v}'. Must be one of: {', '.join(valid)}")
        return v

class HeyGenAvatar(BaseAvatar):
    def __init__(self, **kwargs: Any):
        self.options = HeyGenAvatarOptions(**kwargs)

    @property
    def required_sample_rate(self) -> int:
        return HEYGEN_SAMPLE_RATE

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "api_key": self.options.api_key,
            "quality": self.options.quality,
            "agora_uid": self.options.agora_uid,
        }

        if self.options.agora_token is not None:
            params["agora_token"] = self.options.agora_token
        if self.options.avatar_id is not None:
            params["avatar_id"] = self.options.avatar_id
        if self.options.disable_idle_timeout is not None:
            params["disable_idle_timeout"] = self.options.disable_idle_timeout
        if self.options.activity_idle_timeout is not None:
            params["activity_idle_timeout"] = self.options.activity_idle_timeout
        if self.options.additional_params is not None:
            params = {**self.options.additional_params, **params}

        enable = self.options.enable if self.options.enable is not None else True
        return {"enable": enable, "vendor": "heygen", "params": params}


class AkoolAvatarOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key: str = Field(..., description="Akool API key")
    avatar_id: Optional[str] = Field(default=None, description="Avatar ID")
    enable: Optional[bool] = Field(default=None, description="Enable avatar (default: true)")
    additional_params: Optional[Dict[str, Any]] = Field(default=None, description="Additional vendor-specific parameters")

class AkoolAvatar(BaseAvatar):
    def __init__(self, **kwargs: Any):
        self.options = AkoolAvatarOptions(**kwargs)

    @property
    def required_sample_rate(self) -> int:
        return AKOOL_SAMPLE_RATE

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "api_key": self.options.api_key,
        }

        if self.options.avatar_id is not None:
            params["avatar_id"] = self.options.avatar_id
        if self.options.additional_params is not None:
            params = {**self.options.additional_params, **params}

        enable = self.options.enable if self.options.enable is not None else True
        return {"enable": enable, "vendor": "akool", "params": params}


class LiveAvatarAvatarOptions(HeyGenAvatarOptions):
    pass


class LiveAvatarAvatar(BaseAvatar):
    def __init__(self, **kwargs: Any):
        self.options = LiveAvatarAvatarOptions(**kwargs)

    @property
    def required_sample_rate(self) -> int:
        return LIVEAVATAR_SAMPLE_RATE

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "api_key": self.options.api_key,
            "quality": self.options.quality,
            "agora_uid": self.options.agora_uid,
        }

        if self.options.agora_token is not None:
            params["agora_token"] = self.options.agora_token
        if self.options.avatar_id is not None:
            params["avatar_id"] = self.options.avatar_id
        if self.options.disable_idle_timeout is not None:
            params["disable_idle_timeout"] = self.options.disable_idle_timeout
        if self.options.activity_idle_timeout is not None:
            params["activity_idle_timeout"] = self.options.activity_idle_timeout
        if self.options.additional_params is not None:
            params = {**self.options.additional_params, **params}

        enable = self.options.enable if self.options.enable is not None else True
        return {"enable": enable, "vendor": "liveavatar", "params": params}


class AnamAvatarOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key: str = Field(..., description="Anam API key")
    persona_id: Optional[str] = Field(default=None, description="Persona ID")
    enable: Optional[bool] = Field(default=None, description="Enable avatar (default: true)")
    additional_params: Optional[Dict[str, Any]] = Field(default=None, description="Additional vendor-specific parameters")

class AnamAvatar(BaseAvatar):
    def __init__(self, **kwargs: Any):
        self.options = AnamAvatarOptions(**kwargs)

    @property
    def required_sample_rate(self) -> int:
        return 0

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "api_key": self.options.api_key,
        }

        if self.options.persona_id is not None:
            params["persona_id"] = self.options.persona_id
        if self.options.additional_params is not None:
            params = {**self.options.additional_params, **params}

        enable = self.options.enable if self.options.enable is not None else True
        return {"enable": enable, "vendor": "anam", "params": params}
