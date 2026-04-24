from unittest import mock

import pytest

from agora_agent.agentkit import Agent
from agora_agent.agentkit.vendors import (
    DeepgramSTT,
    ElevenLabsTTS,
    OpenAI,
    OpenAIRealtime,
)
from tests.agentkit.helpers import DummyClient, dump_model


def test_builder_methods_are_immutable_and_reflected_in_config_and_getters():
    agent = Agent(name="base", instructions="helpful")
    llm = OpenAI(api_key="key", model="gpt-4o-mini")
    tts = ElevenLabsTTS(key="tts", model_id="model", voice_id="voice", sample_rate=24000)
    stt = DeepgramSTT(api_key="dg", model="nova-3")

    configured = agent.with_llm(llm).with_tts(tts).with_stt(stt).with_greeting("hi").with_max_history(10)

    assert agent.llm is None
    assert configured.llm == llm.to_config()
    assert configured.tts == tts.to_config()
    assert configured.stt == stt.to_config()
    assert configured.greeting == "hi"
    assert configured.max_history == 10
    assert configured.config["name"] == "base"


def test_create_session_resolves_name_from_option_agent_or_timestamp():
    client = DummyClient()
    named = Agent(name="from-agent")
    explicit = named.create_session(client, channel="c", agent_uid="1", remote_uids=["2"], name="explicit")
    assert explicit.agent.name == "from-agent"
    assert explicit._name == "explicit"

    defaulted = named.create_session(client, channel="c", agent_uid="1", remote_uids=["2"])
    assert defaulted._name == "from-agent"

    with mock.patch("agora_agent.agentkit.agent.time.time", return_value=123456):
        generated = Agent().create_session(client, channel="c", agent_uid="1", remote_uids=["2"])
    assert generated._name == "agent-123456"


def test_to_properties_throws_when_llm_or_tts_missing_outside_preset_or_pipeline_flow():
    with pytest.raises(ValueError, match="TTS configuration is required"):
        Agent().with_llm(OpenAI(api_key="key", model="gpt-4o-mini")).to_properties(
            channel="room",
            agent_uid="1",
            remote_uids=["2"],
            token="token",
        )

    with pytest.raises(ValueError, match="LLM configuration is required"):
        Agent().with_tts(ElevenLabsTTS(key="tts", model_id="model", voice_id="voice", sample_rate=24000)).to_properties(
            channel="room",
            agent_uid="1",
            remote_uids=["2"],
            token="token",
        )


def test_to_properties_applies_defaults_and_overrides_for_standard_pipeline():
    agent = (
        Agent(instructions="top-level instructions", greeting="hello", failure_message="retry", max_history=7)
        .with_llm(
            OpenAI(
                api_key="key",
                model="gpt-4o-mini",
                greeting_message="vendor greeting",
                failure_message="vendor failure",
            )
        )
        .with_tts(ElevenLabsTTS(key="tts", model_id="model", voice_id="voice", sample_rate=24000))
        .with_stt(DeepgramSTT(api_key="dg", model="nova-3"))
    )

    props = dump_model(
        agent.to_properties(channel="room", agent_uid="1", remote_uids=["2"], token="token")
    )

    assert props["llm"]["system_messages"] == [{"role": "system", "content": "top-level instructions"}]
    assert props["llm"]["greeting_message"] == "vendor greeting"
    assert props["llm"]["failure_message"] == "vendor failure"
    assert props["llm"]["max_history"] == 7
    assert props["tts"]["vendor"] == "elevenlabs"
    assert props["asr"]["vendor"] == "deepgram"


def test_to_properties_supports_preset_or_pipeline_backed_sessions_without_llm_or_tts():
    props = dump_model(
        Agent(instructions="preset-backed").to_properties(
            channel="room",
            agent_uid="1",
            remote_uids=["2"],
            token="token",
            skip_vendor_validation=True,
        )
    )
    assert props["channel"] == "room"
    assert "llm" not in props
    assert "tts" not in props


def test_to_properties_generates_token_and_respects_mllm_vendor_precedence():
    agent = Agent(greeting="top hello", failure_message="top fail", max_history=9).with_mllm(
        OpenAIRealtime(
            api_key="key",
            url="wss://openai.example.com/realtime",
            greeting_message="vendor hello",
        )
    ).with_advanced_features({"enable_mllm": True})

    props = dump_model(
        agent.to_properties(
            channel="room",
            agent_uid="1",
            remote_uids=["2"],
            app_id="app-id",
            app_certificate="app-cert",
        )
    )

    assert props["mllm"]["greeting_message"] == "vendor hello"
    assert props["mllm"]["failure_message"] == "top fail"
    assert props["mllm"]["max_history"] == 9
    assert props["mllm"]["url"] == "wss://openai.example.com/realtime"
    assert isinstance(props["token"], str) and props["token"]
