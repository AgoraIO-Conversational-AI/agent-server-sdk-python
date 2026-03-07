from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from typing_extensions import Literal

SampleRate = Literal[8000, 16000, 22050, 24000, 44100, 48000]

ElevenLabsSampleRate = Literal[16000, 22050, 24000, 44100]
MicrosoftSampleRate = Literal[8000, 16000, 24000, 48000]
OpenAISampleRate = Literal[24000]
CartesiaSampleRate = Literal[8000, 16000, 22050, 24000, 44100, 48000]


class BaseLLM(ABC):
    @abstractmethod
    def to_config(self) -> Dict[str, Any]:
        pass


class BaseTTS(ABC):
    @abstractmethod
    def to_config(self) -> Dict[str, Any]:
        pass

    @property
    @abstractmethod
    def sample_rate(self) -> Optional[int]:
        pass


class BaseSTT(ABC):
    @abstractmethod
    def to_config(self) -> Dict[str, Any]:
        pass


class BaseMLLM(ABC):
    @abstractmethod
    def to_config(self) -> Dict[str, Any]:
        pass


class BaseAvatar(ABC):
    @property
    @abstractmethod
    def required_sample_rate(self) -> int:
        pass

    @abstractmethod
    def to_config(self) -> Dict[str, Any]:
        pass
