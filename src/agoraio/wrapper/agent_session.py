import typing
import warnings

from ..core.api_error import ApiError
from .agent import Agent
from .avatar_types import is_akool_avatar, is_heygen_avatar, validate_avatar_config, validate_tts_sample_rate


class AgentSessionOptions(typing.TypedDict, total=False):
    client: typing.Any
    agent: Agent
    app_id: str
    app_certificate: str
    name: str
    channel: str
    token: str
    agent_uid: str
    remote_uids: typing.List[str]
    idle_timeout: int
    enable_string_uid: bool


class AgentSession:
    """Manages the lifecycle of an agent session.

    This class provides a high-level interface for managing agent sessions,
    including starting, stopping, and interacting with the agent.

    Use Agent.create_session() to create a session — this is the recommended
    entry point.

    Examples
    --------
    >>> from agoraio import Agora, Area
    >>> from agoraio.wrapper import Agent
    >>>
    >>> client = Agora(area=Area.US, username="...", password="...")
    >>> agent = Agent(name="assistant", instructions="You are a helpful voice assistant.")
    >>> agent = agent.with_llm("openai/gpt-4").with_tts({"vendor": "elevenlabs", ...})
    >>> session = agent.create_session(client, channel="room-123", agent_uid="1", remote_uids=["100"])
    >>> agent_id = session.start()
    >>> session.say("Hello!")
    >>> session.stop()
    """

    def __init__(
        self,
        client: typing.Any,
        agent: Agent,
        app_id: str,
        name: str,
        channel: str,
        agent_uid: str,
        remote_uids: typing.List[str],
        app_certificate: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        idle_timeout: typing.Optional[int] = None,
        enable_string_uid: typing.Optional[bool] = None,
    ):
        self._client = client
        self._agent = agent
        self._app_id = app_id
        self._app_certificate = app_certificate
        self._name = name
        self._channel = channel
        self._token = token
        self._agent_uid = agent_uid
        self._remote_uids = remote_uids
        self._idle_timeout = idle_timeout
        self._enable_string_uid = enable_string_uid
        self._agent_id: typing.Optional[str] = None
        self._status: str = "idle"
        self._event_handlers: typing.Dict[str, typing.List[typing.Callable[..., None]]] = {}

    @property
    def id(self) -> typing.Optional[str]:
        return self._agent_id

    @property
    def status(self) -> str:
        return self._status

    @property
    def agent(self) -> Agent:
        return self._agent

    @property
    def app_id(self) -> str:
        return self._app_id

    @property
    def raw(self) -> typing.Any:
        """Direct access to the underlying Fern-generated AgentsClient.

        Use this to access any new endpoints that Fern generates without
        waiting for wrapper method updates.
        """
        return self._client.agents

    def _validate_avatar_config(self) -> None:
        agent_config = self._agent.config
        avatar = agent_config.get("avatar")
        tts = agent_config.get("tts")

        if not avatar:
            return

        avatar_dict = avatar if isinstance(avatar, dict) else (avatar.dict() if hasattr(avatar, "dict") else {})

        if avatar_dict.get("enable") is False:
            return

        if is_heygen_avatar(avatar_dict) or is_akool_avatar(avatar_dict):
            validate_avatar_config(avatar_dict)

        tts_params = None
        if tts and isinstance(tts, dict):
            tts_params = tts.get("params")
        elif tts and hasattr(tts, "params"):
            tts_params = tts.params if hasattr(tts, "params") else None

        sample_rate = None
        if tts_params and isinstance(tts_params, dict):
            sample_rate = tts_params.get("sample_rate")
        elif tts_params and hasattr(tts_params, "sample_rate"):
            sample_rate = getattr(tts_params, "sample_rate", None)

        if isinstance(sample_rate, int):
            if is_heygen_avatar(avatar_dict) or is_akool_avatar(avatar_dict):
                validate_tts_sample_rate(avatar_dict, sample_rate)
        elif is_heygen_avatar(avatar_dict):
            warnings.warn(
                "HeyGen avatar detected but TTS sample_rate is not explicitly set. "
                "HeyGen requires 24,000 Hz. Please ensure your TTS provider is configured for 24kHz."
            )
        elif is_akool_avatar(avatar_dict):
            warnings.warn(
                "Akool avatar detected but TTS sample_rate is not explicitly set. "
                "Akool requires 16,000 Hz. Please ensure your TTS provider is configured for 16kHz."
            )

    def start(self) -> str:
        """Start the agent session.

        Returns
        -------
        str
            The agent ID.

        Raises
        ------
        RuntimeError
            If the session is not in a startable state.
        ValueError
            If avatar/TTS configuration is invalid.
        """
        if self._status not in ("idle", "stopped", "error"):
            raise RuntimeError(f"Cannot start session in {self._status} state")

        self._validate_avatar_config()
        self._status = "starting"

        try:
            if self._token:
                token_opts: typing.Dict[str, typing.Any] = {"token": self._token}
            else:
                token_opts = {
                    "app_id": self._app_id,
                    "app_certificate": self._app_certificate,
                }

            properties = self._agent.to_properties(
                channel=self._channel,
                agent_uid=self._agent_uid,
                remote_uids=self._remote_uids,
                idle_timeout=self._idle_timeout,
                enable_string_uid=self._enable_string_uid,
                **token_opts,
            )

            response = self._client.agents.start(
                self._app_id,
                name=self._name,
                properties=properties,
            )

            self._agent_id = response.agent_id if hasattr(response, "agent_id") else None
            self._status = "running"
            self._emit("started", {"agent_id": self._agent_id})
            return self._agent_id or ""
        except Exception as e:
            self._status = "error"
            self._emit("error", e)
            raise

    def stop(self) -> None:
        """Stop the agent session.

        If the agent has already stopped (e.g., crashed or timed out),
        this method will succeed silently rather than throwing an error.
        """
        if self._status != "running":
            raise RuntimeError(f"Cannot stop session in {self._status} state")
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        self._status = "stopping"

        try:
            self._client.agents.stop(self._app_id, self._agent_id)
            self._status = "stopped"
            self._emit("stopped", {"agent_id": self._agent_id})
        except ApiError as e:
            if e.status_code == 404:
                self._status = "stopped"
                self._emit("stopped", {"agent_id": self._agent_id})
                return
            self._status = "error"
            self._emit("error", e)
            raise
        except Exception as e:
            self._status = "error"
            self._emit("error", e)
            raise

    def say(self, text: str, priority: typing.Optional[str] = None, interruptable: typing.Optional[bool] = None) -> None:
        """Send a message to be spoken by the agent.

        Parameters
        ----------
        text : str
            The text to speak.
        priority : str, optional
            Priority of the message (INTERRUPT, APPEND, IGNORE).
        interruptable : bool, optional
            Whether the message can be interrupted.
        """
        if self._status != "running":
            raise RuntimeError(f"Cannot say in {self._status} state")
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        kwargs: typing.Dict[str, typing.Any] = {"text": text}
        if priority is not None:
            kwargs["priority"] = priority
        if interruptable is not None:
            kwargs["interruptable"] = interruptable

        self._client.agents.speak(self._app_id, self._agent_id, **kwargs)

    def interrupt(self) -> None:
        """Interrupt the agent while speaking or thinking."""
        if self._status != "running":
            raise RuntimeError(f"Cannot interrupt in {self._status} state")
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        self._client.agents.interrupt(self._app_id, self._agent_id)

    def update(self, properties: typing.Any) -> None:
        """Update the agent configuration at runtime.

        Parameters
        ----------
        properties : UpdateAgentsRequestProperties
            Partial configuration to update.
        """
        if self._status != "running":
            raise RuntimeError(f"Cannot update in {self._status} state")
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        self._client.agents.update(self._app_id, self._agent_id, properties=properties)

    def get_history(self) -> typing.Any:
        """Get the conversation history."""
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        return self._client.agents.get_history(self._app_id, self._agent_id)

    def get_info(self) -> typing.Any:
        """Get the current session info."""
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        return self._client.agents.get(self._app_id, self._agent_id)

    def on(self, event: str, handler: typing.Callable[..., None]) -> None:
        """Register an event handler.

        Parameters
        ----------
        event : str
            The event type (started, stopped, error).
        handler : callable
            The event handler.
        """
        if event not in self._event_handlers:
            self._event_handlers[event] = []
        self._event_handlers[event].append(handler)

    def off(self, event: str, handler: typing.Callable[..., None]) -> None:
        """Unregister an event handler."""
        handlers = self._event_handlers.get(event)
        if handlers and handler in handlers:
            handlers.remove(handler)

    def _emit(self, event: str, data: typing.Any) -> None:
        handlers = self._event_handlers.get(event)
        if handlers:
            for handler in handlers:
                try:
                    handler(data)
                except Exception:
                    pass


class AsyncAgentSession:
    """Async version of AgentSession for use with AsyncAgora client.

    Examples
    --------
    >>> from agoraio import AsyncAgora, Area
    >>> from agoraio.wrapper import Agent
    >>>
    >>> client = AsyncAgora(area=Area.US, username="...", password="...")
    >>> agent = Agent(name="assistant", instructions="You are helpful.")
    >>> agent = agent.with_llm("openai/gpt-4").with_tts({"vendor": "elevenlabs", ...})
    >>> session = AsyncAgentSession(client=client, agent=agent, ...)
    >>> agent_id = await session.start()
    >>> await session.say("Hello!")
    >>> await session.stop()
    """

    def __init__(
        self,
        client: typing.Any,
        agent: Agent,
        app_id: str,
        name: str,
        channel: str,
        agent_uid: str,
        remote_uids: typing.List[str],
        app_certificate: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        idle_timeout: typing.Optional[int] = None,
        enable_string_uid: typing.Optional[bool] = None,
    ):
        self._client = client
        self._agent = agent
        self._app_id = app_id
        self._app_certificate = app_certificate
        self._name = name
        self._channel = channel
        self._token = token
        self._agent_uid = agent_uid
        self._remote_uids = remote_uids
        self._idle_timeout = idle_timeout
        self._enable_string_uid = enable_string_uid
        self._agent_id: typing.Optional[str] = None
        self._status: str = "idle"
        self._event_handlers: typing.Dict[str, typing.List[typing.Callable[..., None]]] = {}

    @property
    def id(self) -> typing.Optional[str]:
        return self._agent_id

    @property
    def status(self) -> str:
        return self._status

    @property
    def agent(self) -> Agent:
        return self._agent

    @property
    def app_id(self) -> str:
        return self._app_id

    @property
    def raw(self) -> typing.Any:
        """Direct access to the underlying Fern-generated AsyncAgentsClient."""
        return self._client.agents

    def _validate_avatar_config(self) -> None:
        agent_config = self._agent.config
        avatar = agent_config.get("avatar")
        tts = agent_config.get("tts")

        if not avatar:
            return

        avatar_dict = avatar if isinstance(avatar, dict) else (avatar.dict() if hasattr(avatar, "dict") else {})

        if avatar_dict.get("enable") is False:
            return

        if is_heygen_avatar(avatar_dict) or is_akool_avatar(avatar_dict):
            validate_avatar_config(avatar_dict)

        tts_params = None
        if tts and isinstance(tts, dict):
            tts_params = tts.get("params")
        elif tts and hasattr(tts, "params"):
            tts_params = tts.params if hasattr(tts, "params") else None

        sample_rate = None
        if tts_params and isinstance(tts_params, dict):
            sample_rate = tts_params.get("sample_rate")
        elif tts_params and hasattr(tts_params, "sample_rate"):
            sample_rate = getattr(tts_params, "sample_rate", None)

        if isinstance(sample_rate, int):
            if is_heygen_avatar(avatar_dict) or is_akool_avatar(avatar_dict):
                validate_tts_sample_rate(avatar_dict, sample_rate)
        elif is_heygen_avatar(avatar_dict):
            warnings.warn(
                "HeyGen avatar detected but TTS sample_rate is not explicitly set. "
                "HeyGen requires 24,000 Hz."
            )
        elif is_akool_avatar(avatar_dict):
            warnings.warn(
                "Akool avatar detected but TTS sample_rate is not explicitly set. "
                "Akool requires 16,000 Hz."
            )

    async def start(self) -> str:
        """Start the agent session (async).

        Returns
        -------
        str
            The agent ID.
        """
        if self._status not in ("idle", "stopped", "error"):
            raise RuntimeError(f"Cannot start session in {self._status} state")

        self._validate_avatar_config()
        self._status = "starting"

        try:
            if self._token:
                token_opts: typing.Dict[str, typing.Any] = {"token": self._token}
            else:
                token_opts = {
                    "app_id": self._app_id,
                    "app_certificate": self._app_certificate,
                }

            properties = self._agent.to_properties(
                channel=self._channel,
                agent_uid=self._agent_uid,
                remote_uids=self._remote_uids,
                idle_timeout=self._idle_timeout,
                enable_string_uid=self._enable_string_uid,
                **token_opts,
            )

            response = await self._client.agents.start(
                self._app_id,
                name=self._name,
                properties=properties,
            )

            self._agent_id = response.agent_id if hasattr(response, "agent_id") else None
            self._status = "running"
            self._emit("started", {"agent_id": self._agent_id})
            return self._agent_id or ""
        except Exception as e:
            self._status = "error"
            self._emit("error", e)
            raise

    async def stop(self) -> None:
        """Stop the agent session (async)."""
        if self._status != "running":
            raise RuntimeError(f"Cannot stop session in {self._status} state")
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        self._status = "stopping"

        try:
            await self._client.agents.stop(self._app_id, self._agent_id)
            self._status = "stopped"
            self._emit("stopped", {"agent_id": self._agent_id})
        except ApiError as e:
            if e.status_code == 404:
                self._status = "stopped"
                self._emit("stopped", {"agent_id": self._agent_id})
                return
            self._status = "error"
            self._emit("error", e)
            raise
        except Exception as e:
            self._status = "error"
            self._emit("error", e)
            raise

    async def say(self, text: str, priority: typing.Optional[str] = None, interruptable: typing.Optional[bool] = None) -> None:
        """Send a message to be spoken by the agent (async)."""
        if self._status != "running":
            raise RuntimeError(f"Cannot say in {self._status} state")
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        kwargs: typing.Dict[str, typing.Any] = {"text": text}
        if priority is not None:
            kwargs["priority"] = priority
        if interruptable is not None:
            kwargs["interruptable"] = interruptable

        await self._client.agents.speak(self._app_id, self._agent_id, **kwargs)

    async def interrupt(self) -> None:
        """Interrupt the agent while speaking or thinking (async)."""
        if self._status != "running":
            raise RuntimeError(f"Cannot interrupt in {self._status} state")
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        await self._client.agents.interrupt(self._app_id, self._agent_id)

    async def update(self, properties: typing.Any) -> None:
        """Update the agent configuration at runtime (async)."""
        if self._status != "running":
            raise RuntimeError(f"Cannot update in {self._status} state")
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        await self._client.agents.update(self._app_id, self._agent_id, properties=properties)

    async def get_history(self) -> typing.Any:
        """Get the conversation history (async)."""
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        return await self._client.agents.get_history(self._app_id, self._agent_id)

    async def get_info(self) -> typing.Any:
        """Get the current session info (async)."""
        if not self._agent_id:
            raise RuntimeError("No agent ID available")

        return await self._client.agents.get(self._app_id, self._agent_id)

    def on(self, event: str, handler: typing.Callable[..., None]) -> None:
        """Register an event handler."""
        if event not in self._event_handlers:
            self._event_handlers[event] = []
        self._event_handlers[event].append(handler)

    def off(self, event: str, handler: typing.Callable[..., None]) -> None:
        """Unregister an event handler."""
        handlers = self._event_handlers.get(event)
        if handlers and handler in handlers:
            handlers.remove(handler)

    def _emit(self, event: str, data: typing.Any) -> None:
        handlers = self._event_handlers.get(event)
        if handlers:
            for handler in handlers:
                try:
                    handler(data)
                except Exception:
                    pass
