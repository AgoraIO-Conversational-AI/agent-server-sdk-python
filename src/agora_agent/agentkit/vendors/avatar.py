from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator

from .base import BaseAvatar

HEYGEN_SAMPLE_RATE = 24000
AKOOL_SAMPLE_RATE = 16000


class HeyGenAvatarOptions(BaseModel):
    api_key: str = Field(..., description="HeyGen API key")
    quality: str = Field(..., description="Avatar quality: low, medium, or high")
    agora_uid: str = Field(..., description="Agora UID for the avatar stream")
    avatar_name: Optional[str] = Field(default=None, description="Avatar name")
    voice_id: Optional[str] = Field(default=None, description="Voice ID")
    language: Optional[str] = Field(default=None, description="Language code")
    version: Optional[str] = Field(default=None, description="API version (v1 or v2)")

    @field_validator("quality")
    @classmethod
    def validate_quality(cls, v: str) -> str:
        valid = ("low", "medium", "high")
        if v not in valid:
            raise ValueError(f"Invalid quality '{v}'. Must be one of: {', '.join(valid)}")
        return v

    class Config:
        extra = "forbid"


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

        if self.options.avatar_name is not None:
            params["avatar_name"] = self.options.avatar_name
        if self.options.voice_id is not None:
            params["voice_id"] = self.options.voice_id
        if self.options.language is not None:
            params["language"] = self.options.language
        if self.options.version is not None:
            params["version"] = self.options.version

        return {"vendor": "heygen", "params": params}


class AkoolAvatarOptions(BaseModel):
    api_key: str = Field(..., description="Akool API key")
    agora_uid: str = Field(..., description="Agora UID for the avatar stream")
    avatar_id: Optional[str] = Field(default=None, description="Avatar ID")

    class Config:
        extra = "forbid"


class AkoolAvatar(BaseAvatar):
    def __init__(self, **kwargs: Any):
        self.options = AkoolAvatarOptions(**kwargs)

    @property
    def required_sample_rate(self) -> int:
        return AKOOL_SAMPLE_RATE

    def to_config(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "api_key": self.options.api_key,
            "agora_uid": self.options.agora_uid,
        }

        if self.options.avatar_id is not None:
            params["avatar_id"] = self.options.avatar_id

        return {"vendor": "akool", "params": params}
