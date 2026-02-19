from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .agent_session import AgentSession

from ..agents.types.start_agents_request_properties import StartAgentsRequestProperties
from ..agents.types.start_agents_request_properties_asr import StartAgentsRequestPropertiesAsr
from ..agents.types.start_agents_request_properties_avatar import StartAgentsRequestPropertiesAvatar
from ..agents.types.start_agents_request_properties_llm import StartAgentsRequestPropertiesLlm
from ..agents.types.start_agents_request_properties_mllm import StartAgentsRequestPropertiesMllm
from ..agents.types.start_agents_request_properties_parameters import StartAgentsRequestPropertiesParameters
from ..agents.types.start_agents_request_properties_sal import StartAgentsRequestPropertiesSal
from ..agents.types.start_agents_request_properties_turn_detection import StartAgentsRequestPropertiesTurnDetection
from ..types.tts import Tts
from .token import generate_rtc_token

LlmConfig = StartAgentsRequestPropertiesLlm
SttConfig = StartAgentsRequestPropertiesAsr
TtsConfig = Tts
MllmConfig = StartAgentsRequestPropertiesMllm
TurnDetectionConfig = StartAgentsRequestPropertiesTurnDetection
SalConfig = StartAgentsRequestPropertiesSal
AvatarConfig = StartAgentsRequestPropertiesAvatar
AdvancedFeatures = typing.Dict[str, typing.Any]
SessionParams = StartAgentsRequestPropertiesParameters


class AgentOptions(typing.TypedDict, total=False):
    name: str
    instructions: str
    llm: typing.Union[LlmConfig, str]
    tts: typing.Union[TtsConfig, str]
    stt: typing.Union[SttConfig, str]
    mllm: MllmConfig
    turn_detection: TurnDetectionConfig
    sal: SalConfig
    avatar: AvatarConfig
    advanced_features: AdvancedFeatures
    parameters: SessionParams
    greeting: str
    failure_message: str
    max_history: int


VENDOR_URLS: typing.Dict[str, str] = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "anthropic": "https://api.anthropic.com/v1/messages",
    "azure": "https://YOUR_RESOURCE.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT/chat/completions",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/models",
}

STT_VENDOR_MAP: typing.Dict[str, str] = {
    "ares": "ares",
    "microsoft": "microsoft",
    "deepgram": "deepgram",
    "openai": "openai",
    "google": "google",
    "amazon": "amazon",
    "assemblyai": "assemblyai",
    "speechmatics": "speechmatics",
}


def _parse_llm_shorthand(shorthand: str) -> LlmConfig:
    parts = shorthand.split("/", 1)
    vendor = parts[0].lower() if parts else ""
    model = parts[1] if len(parts) > 1 else None

    url = VENDOR_URLS.get(vendor, VENDOR_URLS["openai"])
    style: typing.Optional[str] = None
    if vendor in ("gemini", "anthropic"):
        style = vendor
    else:
        style = "openai"

    return LlmConfig(
        url=url,
        vendor="azure" if vendor == "azure" else None,
        style=style,
        params={"model": model} if model else None,
    )


def _parse_stt_shorthand(shorthand: str) -> SttConfig:
    parts = shorthand.split("/", 1)
    vendor = parts[0].lower() if parts else ""
    return SttConfig(
        vendor=STT_VENDOR_MAP.get(vendor, "deepgram"),
    )


def _parse_tts_shorthand(shorthand: str) -> typing.Dict[str, typing.Any]:
    parts = shorthand.split("/", 1)
    vendor_lower = parts[0].lower() if parts else ""
    voice_or_model = parts[1] if len(parts) > 1 else None

    if vendor_lower == "microsoft":
        return {
            "vendor": "microsoft",
            "params": {
                "key": "",
                "region": "eastus",
                "voice_name": voice_or_model or "en-US-JennyNeural",
            },
        }
    elif vendor_lower == "elevenlabs":
        return {
            "vendor": "elevenlabs",
            "params": {
                "key": "",
                "model_id": "eleven_flash_v2_5",
                "voice_id": voice_or_model or "",
            },
        }
    elif vendor_lower == "openai":
        return {
            "vendor": "openai",
            "params": {
                "key": "",
                "voice": voice_or_model or "alloy",
            },
        }
    elif vendor_lower == "cartesia":
        return {
            "vendor": "cartesia",
            "params": {
                "key": "",
                "voice_id": voice_or_model or "",
            },
        }
    elif vendor_lower == "google":
        return {
            "vendor": "google",
            "params": {
                "key": "",
                "voice_name": voice_or_model or "",
            },
        }
    elif vendor_lower == "amazon":
        return {
            "vendor": "amazon",
            "params": {
                "access_key": "",
                "secret_key": "",
                "region": "us-east-1",
                "voice_id": voice_or_model or "",
            },
        }
    else:
        return {
            "vendor": "microsoft",
            "params": {
                "key": "",
                "region": "eastus",
                "voice_name": voice_or_model or "en-US-JennyNeural",
            },
        }


class Agent:
    """A reusable agent definition.

    This class represents an agent configuration that can be used to create
    multiple sessions. It provides a fluent builder pattern for configuration.

    Examples
    --------
    >>> agent = Agent(
    ...     instructions="You are a helpful voice assistant.",
    ...     llm="openai/gpt-4-turbo",
    ...     stt="deepgram/nova-2",
    ... )

    >>> agent = Agent(instructions="You are helpful.").with_llm("openai/gpt-4")
    """

    def __init__(
        self,
        name: typing.Optional[str] = None,
        instructions: typing.Optional[str] = None,
        llm: typing.Optional[typing.Union[LlmConfig, str]] = None,
        tts: typing.Optional[typing.Union[TtsConfig, str]] = None,
        stt: typing.Optional[typing.Union[SttConfig, str]] = None,
        mllm: typing.Optional[MllmConfig] = None,
        turn_detection: typing.Optional[TurnDetectionConfig] = None,
        sal: typing.Optional[SalConfig] = None,
        avatar: typing.Optional[AvatarConfig] = None,
        advanced_features: typing.Optional[AdvancedFeatures] = None,
        parameters: typing.Optional[SessionParams] = None,
        greeting: typing.Optional[str] = None,
        failure_message: typing.Optional[str] = None,
        max_history: typing.Optional[int] = None,
    ):
        self._name = name
        self._instructions = instructions
        self._greeting = greeting
        self._failure_message = failure_message
        self._max_history = max_history
        self._llm: typing.Optional[LlmConfig] = None
        self._tts: typing.Optional[typing.Any] = None
        self._stt: typing.Optional[SttConfig] = None
        self._mllm = mllm
        self._turn_detection = turn_detection
        self._sal = sal
        self._avatar = avatar
        self._advanced_features = advanced_features
        self._parameters = parameters

        if llm is not None:
            self._llm = _parse_llm_shorthand(llm) if isinstance(llm, str) else llm
        if tts is not None:
            self._tts = _parse_tts_shorthand(tts) if isinstance(tts, str) else tts
        if stt is not None:
            self._stt = _parse_stt_shorthand(stt) if isinstance(stt, str) else stt

    def with_llm(self, config: typing.Union[LlmConfig, str]) -> "Agent":
        new_agent = self._clone()
        new_agent._llm = _parse_llm_shorthand(config) if isinstance(config, str) else config
        return new_agent

    def with_tts(self, config: typing.Union[TtsConfig, str]) -> "Agent":
        new_agent = self._clone()
        new_agent._tts = _parse_tts_shorthand(config) if isinstance(config, str) else config
        return new_agent

    def with_stt(self, config: typing.Union[SttConfig, str]) -> "Agent":
        new_agent = self._clone()
        new_agent._stt = _parse_stt_shorthand(config) if isinstance(config, str) else config
        return new_agent

    def with_mllm(self, config: MllmConfig) -> "Agent":
        new_agent = self._clone()
        new_agent._mllm = config
        return new_agent

    def with_turn_detection(self, config: TurnDetectionConfig) -> "Agent":
        new_agent = self._clone()
        new_agent._turn_detection = config
        return new_agent

    def with_instructions(self, instructions: str) -> "Agent":
        new_agent = self._clone()
        new_agent._instructions = instructions
        return new_agent

    def with_greeting(self, greeting: str) -> "Agent":
        new_agent = self._clone()
        new_agent._greeting = greeting
        return new_agent

    def with_name(self, name: str) -> "Agent":
        new_agent = self._clone()
        new_agent._name = name
        return new_agent

    @property
    def name(self) -> typing.Optional[str]:
        return self._name

    @property
    def llm(self) -> typing.Optional[LlmConfig]:
        return self._llm

    @property
    def tts(self) -> typing.Optional[typing.Any]:
        return self._tts

    @property
    def stt(self) -> typing.Optional[SttConfig]:
        return self._stt

    @property
    def mllm(self) -> typing.Optional[MllmConfig]:
        return self._mllm

    @property
    def turn_detection(self) -> typing.Optional[TurnDetectionConfig]:
        return self._turn_detection

    @property
    def instructions(self) -> typing.Optional[str]:
        return self._instructions

    @property
    def greeting(self) -> typing.Optional[str]:
        return self._greeting

    @property
    def config(self) -> typing.Dict[str, typing.Any]:
        return {
            "name": self._name,
            "instructions": self._instructions,
            "llm": self._llm,
            "tts": self._tts,
            "stt": self._stt,
            "mllm": self._mllm,
            "turn_detection": self._turn_detection,
            "sal": self._sal,
            "avatar": self._avatar,
            "advanced_features": self._advanced_features,
            "parameters": self._parameters,
            "greeting": self._greeting,
            "failure_message": self._failure_message,
            "max_history": self._max_history,
        }

    def create_session(
        self,
        client: typing.Any,
        channel: str,
        agent_uid: str,
        remote_uids: typing.List[str],
        name: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        idle_timeout: typing.Optional[int] = None,
        enable_string_uid: typing.Optional[bool] = None,
    ) -> "AgentSession":
        from .agent_session import AgentSession

        session_name = name or self._name or f"agent-{int(typing.cast(typing.Any, __import__('time')).time())}"
        return AgentSession(
            client=client,
            agent=self,
            app_id=client.app_id if hasattr(client, "app_id") else "",
            app_certificate=client.app_certificate if hasattr(client, "app_certificate") else None,
            name=session_name,
            channel=channel,
            token=token,
            agent_uid=agent_uid,
            remote_uids=remote_uids,
            idle_timeout=idle_timeout,
            enable_string_uid=enable_string_uid,
        )

    def to_properties(
        self,
        channel: str,
        agent_uid: str,
        remote_uids: typing.List[str],
        idle_timeout: typing.Optional[int] = None,
        enable_string_uid: typing.Optional[bool] = None,
        token: typing.Optional[str] = None,
        app_id: typing.Optional[str] = None,
        app_certificate: typing.Optional[str] = None,
        token_expiry_seconds: typing.Optional[int] = None,
    ) -> StartAgentsRequestProperties:
        if token is None:
            if app_id is None or app_certificate is None:
                raise ValueError("Either token or app_id+app_certificate must be provided")
            token = generate_rtc_token(
                app_id=app_id,
                app_certificate=app_certificate,
                channel=channel,
                uid=int(agent_uid),
                expiry_seconds=token_expiry_seconds or 3600,
            )

        is_mllm_mode = (
            self._advanced_features is not None
            and isinstance(self._advanced_features, dict)
            and self._advanced_features.get("enable_mllm") is True
        )

        base_kwargs: typing.Dict[str, typing.Any] = {
            "channel": channel,
            "token": token,
            "agent_rtc_uid": agent_uid,
            "remote_rtc_uids": remote_uids,
        }

        if idle_timeout is not None:
            base_kwargs["idle_timeout"] = idle_timeout
        if enable_string_uid is not None:
            base_kwargs["enable_string_uid"] = enable_string_uid
        if self._mllm is not None:
            base_kwargs["mllm"] = self._mllm
        if self._turn_detection is not None:
            base_kwargs["turn_detection"] = self._turn_detection
        if self._sal is not None:
            base_kwargs["sal"] = self._sal
        if self._avatar is not None:
            base_kwargs["avatar"] = self._avatar
        if self._advanced_features is not None:
            base_kwargs["advanced_features"] = self._advanced_features
        if self._parameters is not None:
            base_kwargs["parameters"] = self._parameters

        if is_mllm_mode:
            return StartAgentsRequestProperties(**base_kwargs)

        if self._tts is None:
            raise ValueError("TTS configuration is required. Use with_tts() to set it.")

        if self._llm is None:
            raise ValueError("LLM configuration is required. Use with_llm() to set it.")

        llm_kwargs: typing.Dict[str, typing.Any] = {}
        if isinstance(self._llm, LlmConfig):
            llm_dict = self._llm.dict(exclude_none=True) if hasattr(self._llm, "dict") else {}
            llm_kwargs.update(llm_dict)
        if self._instructions:
            llm_kwargs["system_messages"] = [{"role": "system", "content": self._instructions}]
        if self._greeting:
            llm_kwargs.setdefault("greeting_message", self._greeting)
        if self._failure_message:
            llm_kwargs.setdefault("failure_message", self._failure_message)
        if self._max_history is not None:
            llm_kwargs.setdefault("max_history", self._max_history)

        base_kwargs["llm"] = LlmConfig(**llm_kwargs) if llm_kwargs.get("url") else self._llm
        base_kwargs["tts"] = self._tts
        if self._stt is not None:
            base_kwargs["asr"] = self._stt

        return StartAgentsRequestProperties(**base_kwargs)

    def _clone(self) -> "Agent":
        new_agent = Agent.__new__(Agent)
        new_agent._name = self._name
        new_agent._llm = self._llm
        new_agent._tts = self._tts
        new_agent._stt = self._stt
        new_agent._mllm = self._mllm
        new_agent._turn_detection = self._turn_detection
        new_agent._sal = self._sal
        new_agent._avatar = self._avatar
        new_agent._advanced_features = self._advanced_features
        new_agent._parameters = self._parameters
        new_agent._instructions = self._instructions
        new_agent._greeting = self._greeting
        new_agent._failure_message = self._failure_message
        new_agent._max_history = self._max_history
        return new_agent
