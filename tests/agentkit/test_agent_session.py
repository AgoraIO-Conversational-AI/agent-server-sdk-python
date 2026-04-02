import asyncio
from unittest import mock

import pytest

from agora_agent.agentkit import Agent
from agora_agent.agentkit.vendors import AkoolAvatar, DeepgramSTT, ElevenLabsTTS, OpenAI
from agora_agent.core.api_error import ApiError
from tests.agentkit.helpers import DummyAsyncClient, DummyClient, dump_model


def build_standard_agent():
    return (
        Agent(name="assistant", instructions="be helpful")
        .with_stt(DeepgramSTT(api_key="dg", model="nova-3"))
        .with_llm(OpenAI(api_key="key", model="gpt-4o-mini"))
        .with_tts(ElevenLabsTTS(key="tts", model_id="model", voice_id="voice", sample_rate=24000))
    )


def test_start_accepts_preset_arrays_and_normalizes_them():
    client = DummyClient()
    session = Agent(name="assistant").create_session(
        client,
        channel="room",
        agent_uid="1",
        remote_uids=["2"],
        preset=["deepgram_nova_3", "openai_gpt_5_mini", "openai_tts_1"],
    )
    session.start()
    _, kwargs = client.agents.start_calls[0]
    assert kwargs["preset"] == "deepgram_nova_3,openai_gpt_5_mini,openai_tts_1"


def test_session_methods_enforce_state_and_id_guards():
    session = build_standard_agent().create_session(DummyClient(), channel="room", agent_uid="1", remote_uids=["2"])

    for method_name in ["stop", "interrupt", "update", "say"]:
        with pytest.raises(RuntimeError):
            if method_name == "say":
                getattr(session, method_name)("hello")
            elif method_name == "update":
                getattr(session, method_name)({})
            else:
                getattr(session, method_name)()

    with pytest.raises(RuntimeError):
        session.get_history()
    with pytest.raises(RuntimeError):
        session.get_info()
    with pytest.raises(RuntimeError):
        session.get_turns()


def test_app_credentials_mode_adds_auth_headers_and_exposes_getters_and_raw_client():
    client = DummyClient(auth_mode="app-credentials")
    session = build_standard_agent().create_session(client, channel="room", agent_uid="1", remote_uids=["2"])

    headers = session._convo_ai_headers()
    assert headers is not None
    assert headers["Authorization"].startswith("agora token=")
    assert session.app_id == "app-id"
    assert session.agent.name == "assistant"
    assert session.raw is client.agents


def test_event_handlers_can_be_added_removed_and_warning_path_exercised():
    client = DummyClient()
    session = build_standard_agent().create_session(client, channel="room", agent_uid="1", remote_uids=["2"])
    received = []

    def started(payload):
        received.append(payload)

    def failing(_payload):
        raise RuntimeError("boom")

    session.on("started", started)
    session.on("started", failing)

    with pytest.warns(UserWarning):
        session.start()

    assert received == [{"agent_id": "agent-1"}]
    session.off("started", started)
    session._emit("started", {"agent_id": "agent-2"})
    assert received == [{"agent_id": "agent-1"}]


def test_running_session_methods_call_underlying_client_helpers():
    client = DummyClient()
    session = build_standard_agent().create_session(client, channel="room", agent_uid="1", remote_uids=["2"])
    session.start()
    session.say("hello", priority="APPEND", interruptable=True)
    session.interrupt()
    session.update({"greeting_message": "updated"})
    assert session.get_history() == {"contents": []}
    assert session.get_info() == {"agent_id": "agent-1"}
    assert session.get_turns() == {"turns": [{"agent_id": "agent-1"}]}
    session.stop()

    assert client.agents.speak_calls
    assert client.agents.interrupt_calls
    assert client.agents.update_calls
    assert client.agents.history_calls
    assert client.agents.get_calls
    assert client.agents.turn_calls
    assert client.agents.stop_calls


def test_start_sets_status_to_error_and_emits_error_event_on_failure():
    client = DummyClient()
    client.agents.start_error = RuntimeError("start failed")
    session = build_standard_agent().create_session(client, channel="room", agent_uid="1", remote_uids=["2"])
    errors = []
    session.on("error", errors.append)

    with pytest.raises(RuntimeError, match="start failed"):
        session.start()

    assert session.status == "error"
    assert len(errors) == 1


def test_stop_swallows_404_and_non_404_moves_to_error():
    client = DummyClient()
    session = build_standard_agent().create_session(client, channel="room", agent_uid="1", remote_uids=["2"])
    session.start()
    client.agents.stop_error = ApiError(status_code=404)
    session.stop()
    assert session.status == "stopped"

    client2 = DummyClient()
    session2 = build_standard_agent().create_session(client2, channel="room", agent_uid="1", remote_uids=["2"])
    session2.start()
    client2.agents.stop_error = ApiError(status_code=500)
    with pytest.raises(ApiError):
        session2.stop()
    assert session2.status == "error"


def test_avatar_validation_warning_branch_and_async_session_methods():
    agent = (
        Agent(name="avatar")
        .with_llm(OpenAI(api_key="key", model="gpt-4o-mini"))
        .with_tts(ElevenLabsTTS(key="tts", model_id="model", voice_id="voice"))
        .with_avatar(AkoolAvatar(api_key="akool", avatar_id="avatar-1"))
    )
    client = DummyClient()
    session = agent.create_session(client, channel="room", agent_uid="1", remote_uids=["2"])
    with pytest.warns(UserWarning):
        session._validate_avatar_config()

    async def run_async_case():
        async_client = DummyAsyncClient()
        async_session = build_standard_agent().create_async_session(
            async_client,
            channel="room",
            agent_uid="1",
            remote_uids=["2"],
        )
        await async_session.start()
        await async_session.say("hello")
        await async_session.interrupt()
        await async_session.update({"greeting_message": "updated"})
        assert await async_session.get_history() == {"contents": []}
        assert await async_session.get_info() == {"agent_id": "agent-1"}
        assert await async_session.get_turns() == {"turns": [{"agent_id": "agent-1"}]}
        await async_session.stop()

    asyncio.run(run_async_case())
