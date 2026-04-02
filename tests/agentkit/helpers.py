from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Dict, List, Optional


def dump_model(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(exclude_none=True)
    if isinstance(value, dict):
        return {k: dump_model(v) for k, v in value.items()}
    if isinstance(value, list):
        return [dump_model(v) for v in value]
    return value


class DummyAgents:
    def __init__(self) -> None:
        self.start_calls: List[Any] = []
        self.stop_calls: List[Any] = []
        self.speak_calls: List[Any] = []
        self.interrupt_calls: List[Any] = []
        self.update_calls: List[Any] = []
        self.history_calls: List[Any] = []
        self.turn_calls: List[Any] = []
        self.get_calls: List[Any] = []

        self.start_result: Any = SimpleNamespace(agent_id="agent-1")
        self.start_error: Optional[Exception] = None
        self.stop_error: Optional[Exception] = None

    def start(self, app_id, **kwargs):
        self.start_calls.append((app_id, kwargs))
        if self.start_error is not None:
            raise self.start_error
        return self.start_result

    def stop(self, app_id, agent_id, request_options=None):
        self.stop_calls.append((app_id, agent_id, request_options))
        if self.stop_error is not None:
            raise self.stop_error
        return None

    def speak(self, app_id, agent_id, request_options=None, **kwargs):
        self.speak_calls.append((app_id, agent_id, request_options, kwargs))
        return None

    def interrupt(self, app_id, agent_id, request_options=None):
        self.interrupt_calls.append((app_id, agent_id, request_options))
        return None

    def update(self, app_id, agent_id, properties=None, request_options=None):
        self.update_calls.append((app_id, agent_id, properties, request_options))
        return None

    def get_history(self, app_id, agent_id, request_options=None):
        self.history_calls.append((app_id, agent_id, request_options))
        return {"contents": []}

    def get_turns(self, app_id, agent_id, request_options=None):
        self.turn_calls.append((app_id, agent_id, request_options))
        return {"turns": [{"agent_id": agent_id}]}

    def get(self, app_id, agent_id, request_options=None):
        self.get_calls.append((app_id, agent_id, request_options))
        return {"agent_id": agent_id}


class DummyAsyncAgents(DummyAgents):
    async def start(self, app_id, **kwargs):
        return super().start(app_id, **kwargs)

    async def stop(self, app_id, agent_id, request_options=None):
        return super().stop(app_id, agent_id, request_options)

    async def speak(self, app_id, agent_id, request_options=None, **kwargs):
        return super().speak(app_id, agent_id, request_options, **kwargs)

    async def interrupt(self, app_id, agent_id, request_options=None):
        return super().interrupt(app_id, agent_id, request_options)

    async def update(self, app_id, agent_id, properties=None, request_options=None):
        return super().update(app_id, agent_id, properties, request_options)

    async def get_history(self, app_id, agent_id, request_options=None):
        return super().get_history(app_id, agent_id, request_options)

    async def get_turns(self, app_id, agent_id, request_options=None):
        return super().get_turns(app_id, agent_id, request_options)

    async def get(self, app_id, agent_id, request_options=None):
        return super().get(app_id, agent_id, request_options)


class DummyClient:
    def __init__(
        self,
        *,
        auth_mode: str = "basic",
        app_id: str = "app-id",
        app_certificate: Optional[str] = "app-cert",
    ) -> None:
        self.app_id = app_id
        self.app_certificate = app_certificate
        self.auth_mode = auth_mode
        self.agents = DummyAgents()


class DummyAsyncClient(DummyClient):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.agents = DummyAsyncAgents()
