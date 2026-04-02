from types import SimpleNamespace
import unittest

from agora_agent.agentkit import (
    Agent,
    AnamAvatar,
    GeminiLive,
    LiveAvatarAvatar,
    OpenAI,
    OpenAITTS,
    validate_avatar_config,
    validate_tts_sample_rate,
)
from agora_agent.agentkit.vendors import DeepgramSTT


class DummyAgents:
    def __init__(self) -> None:
        self.start_calls = []
        self.turn_calls = []

    def start(self, app_id, **kwargs):
        self.start_calls.append((app_id, kwargs))
        return SimpleNamespace(agent_id="agent-1")

    def get_turns(self, app_id, agent_id, request_options=None):
        self.turn_calls.append((app_id, agent_id, request_options))
        return {"turns": [{"agent_id": agent_id}]}

    def stop(self, *args, **kwargs):
        return None

    def speak(self, *args, **kwargs):
        return None

    def interrupt(self, *args, **kwargs):
        return None

    def update(self, *args, **kwargs):
        return None

    def get_history(self, *args, **kwargs):
        return {"contents": []}

    def get(self, *args, **kwargs):
        return {"agent_id": "agent-1"}


class DummyClient:
    def __init__(self) -> None:
        self.app_id = "app-id"
        self.app_certificate = "app-cert"
        self.auth_mode = "basic"
        self.agents = DummyAgents()


def dump_properties(properties):
    if hasattr(properties, "model_dump"):
        return properties.model_dump(exclude_none=True)
    return properties


class AgentKitParityTests(unittest.TestCase):
    def test_start_supports_preset_and_pipeline_without_explicit_llm_or_tts(self):
        client = DummyClient()
        agent = Agent(name="preset-agent", instructions="Use preset defaults.")

        session = agent.create_session(
            client,
            channel="room-1",
            agent_uid="1",
            remote_uids=["2"],
            preset="deepgram_nova_3,openai_gpt_4o_mini,openai_tts_1",
            pipeline_id="pipeline_123",
        )

        agent_id = session.start()

        self.assertEqual(agent_id, "agent-1")
        _, kwargs = client.agents.start_calls[0]
        self.assertEqual(kwargs["preset"], "deepgram_nova_3,openai_gpt_4o_mini,openai_tts_1")
        self.assertEqual(kwargs["pipeline_id"], "pipeline_123")
        dumped = dump_properties(kwargs["properties"])
        self.assertEqual(dumped["channel"], "room-1")
        self.assertEqual(dumped["agent_rtc_uid"], "1")
        self.assertNotIn("llm", dumped)
        self.assertNotIn("tts", dumped)

    def test_start_infers_reseller_presets_and_strips_credential_fields(self):
        client = DummyClient()
        agent = (
            Agent(name="auto-preset", instructions="Use reseller defaults.")
            .with_stt(DeepgramSTT(model="nova-3"))
            .with_llm(OpenAI(model="gpt-5-mini"))
            .with_tts(OpenAITTS(voice="alloy"))
        )

        session = agent.create_session(
            client,
            channel="room-2",
            agent_uid="1",
            remote_uids=["2"],
        )

        session.start()

        _, kwargs = client.agents.start_calls[0]
        self.assertEqual(kwargs["preset"], "deepgram_nova_3,openai_gpt_5_mini,openai_tts_1")
        dumped = dump_properties(kwargs["properties"])
        self.assertFalse(dumped["asr"].get("params"))
        self.assertEqual(
            dumped["llm"]["system_messages"],
            [{"role": "system", "content": "Use reseller defaults."}],
        )
        self.assertEqual(dumped["llm"]["input_modalities"], ["text"])
        self.assertFalse(dumped["llm"].get("api_key"))
        self.assertEqual(dumped["tts"].get("params"), {"voice": "alloy"})

    def test_session_get_turns_proxies_to_agents_client(self):
        client = DummyClient()
        session = Agent(name="assistant").create_session(
            client,
            channel="room-3",
            agent_uid="1",
            remote_uids=["2"],
            preset="deepgram_nova_3,openai_gpt_4o_mini,openai_tts_1",
        )
        session.start()

        turns = session.get_turns()

        self.assertEqual(turns, {"turns": [{"agent_id": "agent-1"}]})
        self.assertEqual(client.agents.turn_calls, [("app-id", "agent-1", None)])

    def test_gemini_live_matches_low_level_shape(self):
        config = GeminiLive(
            api_key="google-key",
            model="gemini-live-2.5-flash",
            instructions="You are concise.",
            voice="Aoede",
            greeting_message="Hello",
            additional_params={"temperature": 0.2},
            messages=[{"role": "user", "content": "Hi"}],
        ).to_config()

        self.assertEqual(
            config,
            {
                "vendor": "gemini",
                "style": "openai",
                "api_key": "google-key",
                "params": {
                    "temperature": 0.2,
                    "model": "gemini-live-2.5-flash",
                    "instructions": "You are concise.",
                    "voice": "Aoede",
                },
                "messages": [{"role": "user", "content": "Hi"}],
                "greeting_message": "Hello",
            },
        )

    def test_liveavatar_and_anam_avatar_support_matches_typescript(self):
        liveavatar = LiveAvatarAvatar(api_key="live-key", quality="high", agora_uid="42").to_config()
        validate_avatar_config(liveavatar)
        with self.assertRaisesRegex(ValueError, "LiveAvatar"):
            validate_tts_sample_rate(liveavatar, 16000)

        anam = AnamAvatar(api_key="anam-key", persona_id="persona-1").to_config()
        validate_avatar_config(anam)
        agent = Agent().with_tts(OpenAITTS(api_key="openai-key", voice="alloy")).with_avatar(
            AnamAvatar(api_key="anam-key", persona_id="persona-1")
        )
        self.assertEqual(agent.avatar, anam)


if __name__ == "__main__":
    unittest.main()
