from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .agent_session import AgentSession

from ..agents.types.start_agents_request_properties import StartAgentsRequestProperties
from ..agents.types.start_agents_request_properties_turn_detection import StartAgentsRequestPropertiesTurnDetection
from ..agents.types.start_agents_request_properties_sal import StartAgentsRequestPropertiesSal
from ..agents.types.start_agents_request_properties_parameters import StartAgentsRequestPropertiesParameters
from .token import generate_rtc_token
from .vendors.base import BaseAvatar, BaseLLM, BaseMLLM, BaseSTT, BaseTTS

TurnDetectionConfig = StartAgentsRequestPropertiesTurnDetection
SalConfig = StartAgentsRequestPropertiesSal
AdvancedFeatures = typing.Dict[str, typing.Any]
SessionParams = StartAgentsRequestPropertiesParameters


class Agent:
    """A reusable agent definition.

    Use the fluent builder methods (.with_llm(), .with_tts(), .with_stt(), .with_mllm())
    to configure vendor settings after construction.

    Examples
    --------
    >>> from agoraio.wrapper import Agent
    >>> from agoraio.wrapper.vendors import OpenAI, ElevenLabsTTS, DeepgramSTT
    >>>
    >>> agent = Agent(instructions="You are a helpful voice assistant.")
    >>> agent = (
    ...     agent
    ...     .with_llm(OpenAI(api_key="...", model="gpt-4"))
    ...     .with_tts(ElevenLabsTTS(key="...", model_id="...", voice_id="...", sample_rate=24000))
    ...     .with_stt(DeepgramSTT(api_key="...", model="nova-2"))
    ... )
    """

    def __init__(
        self,
        name: typing.Optional[str] = None,
        instructions: typing.Optional[str] = None,
        turn_detection: typing.Optional[TurnDetectionConfig] = None,
        sal: typing.Optional[SalConfig] = None,
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
        self._llm: typing.Optional[typing.Dict[str, typing.Any]] = None
        self._tts: typing.Optional[typing.Dict[str, typing.Any]] = None
        self._stt: typing.Optional[typing.Dict[str, typing.Any]] = None
        self._mllm: typing.Optional[typing.Dict[str, typing.Any]] = None
        self._tts_sample_rate: typing.Optional[int] = None
        self._avatar: typing.Optional[typing.Dict[str, typing.Any]] = None
        self._avatar_required_sample_rate: typing.Optional[int] = None
        self._turn_detection = turn_detection
        self._sal = sal
        self._advanced_features = advanced_features
        self._parameters = parameters

    def with_llm(self, vendor: BaseLLM) -> "Agent":
        new_agent = self._clone()
        new_agent._llm = vendor.to_config()
        return new_agent

    def with_tts(self, vendor: BaseTTS) -> "Agent":
        new_agent = self._clone()
        new_agent._tts = vendor.to_config()
        new_agent._tts_sample_rate = vendor.sample_rate
        return new_agent

    def with_stt(self, vendor: BaseSTT) -> "Agent":
        new_agent = self._clone()
        new_agent._stt = vendor.to_config()
        return new_agent

    def with_mllm(self, vendor: BaseMLLM) -> "Agent":
        new_agent = self._clone()
        new_agent._mllm = vendor.to_config()
        return new_agent

    def with_avatar(self, vendor: BaseAvatar) -> "Agent":
        if self._tts_sample_rate is not None and self._tts_sample_rate != vendor.required_sample_rate:
            raise ValueError(
                f"Avatar requires TTS sample rate of {vendor.required_sample_rate} Hz, "
                f"but TTS is configured with {self._tts_sample_rate} Hz. "
                f"Please update your TTS sample_rate to {vendor.required_sample_rate}."
            )
        new_agent = self._clone()
        new_agent._avatar = vendor.to_config()
        new_agent._avatar_required_sample_rate = vendor.required_sample_rate
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
    def llm(self) -> typing.Optional[typing.Dict[str, typing.Any]]:
        return self._llm

    @property
    def tts(self) -> typing.Optional[typing.Dict[str, typing.Any]]:
        return self._tts

    @property
    def stt(self) -> typing.Optional[typing.Dict[str, typing.Any]]:
        return self._stt

    @property
    def mllm(self) -> typing.Optional[typing.Dict[str, typing.Any]]:
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

        llm_config = dict(self._llm)
        if self._instructions:
            llm_config["system_messages"] = [{"role": "system", "content": self._instructions}]
        if self._greeting:
            llm_config.setdefault("greeting_message", self._greeting)
        if self._failure_message:
            llm_config.setdefault("failure_message", self._failure_message)
        if self._max_history is not None:
            llm_config.setdefault("max_history", self._max_history)

        base_kwargs["llm"] = llm_config
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
        new_agent._tts_sample_rate = self._tts_sample_rate
        new_agent._avatar = self._avatar
        new_agent._avatar_required_sample_rate = self._avatar_required_sample_rate
        new_agent._turn_detection = self._turn_detection
        new_agent._sal = self._sal
        new_agent._advanced_features = self._advanced_features
        new_agent._parameters = self._parameters
        new_agent._instructions = self._instructions
        new_agent._greeting = self._greeting
        new_agent._failure_message = self._failure_message
        new_agent._max_history = self._max_history
        return new_agent
