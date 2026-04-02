from agora_agent.agentkit import AgentPresets, normalize_preset_input
from agora_agent.agentkit.presets import resolve_session_presets


def test_preset_values_match_expected_strings():
    assert AgentPresets.asr.deepgram_nova_2 == "deepgram_nova_2"
    assert AgentPresets.asr.deepgram_nova_3 == "deepgram_nova_3"
    assert AgentPresets.llm.openai_gpt_4o_mini == "openai_gpt_4o_mini"
    assert AgentPresets.llm.openai_gpt_4_1_mini == "openai_gpt_4_1_mini"
    assert AgentPresets.llm.openai_gpt_5_nano == "openai_gpt_5_nano"
    assert AgentPresets.llm.openai_gpt_5_mini == "openai_gpt_5_mini"
    assert AgentPresets.tts.minimax_speech_2_6_turbo == "minimax_speech_2_6_turbo"
    assert AgentPresets.tts.minimax_speech_2_8_turbo == "minimax_speech_2_8_turbo"
    assert AgentPresets.tts.openai_tts_1 == "openai_tts_1"


def test_normalize_preset_input_variants():
    assert normalize_preset_input(None) is None
    assert normalize_preset_input("deepgram_nova_3") == "deepgram_nova_3"
    assert (
        normalize_preset_input(["deepgram_nova_3", "openai_gpt_5_mini"])
        == "deepgram_nova_3,openai_gpt_5_mini"
    )
    assert (
        normalize_preset_input(" deepgram_nova_3, , openai_gpt_5_mini ")
        == "deepgram_nova_3,openai_gpt_5_mini"
    )


def test_resolve_session_presets_returns_none_when_nothing_inferrable():
    preset, properties = resolve_session_presets(None, {"llm": {"vendor": "custom"}})
    assert preset is None
    assert properties["llm"] == {"vendor": "custom"}
    assert properties["asr"] is None
    assert properties["tts"] is None


def test_resolve_session_presets_inferrs_and_strips_fields():
    preset, properties = resolve_session_presets(
        None,
        {
            "asr": {"vendor": "deepgram", "params": {"model": "nova-3"}},
            "llm": {
                "vendor": "openai",
                "url": "https://api.openai.com/v1/chat/completions",
                "params": {"model": "gpt-5-mini"},
            },
            "tts": {"vendor": "openai", "params": {"model": "tts-1", "voice": "alloy"}},
        },
    )
    assert preset == "deepgram_nova_3,openai_gpt_5_mini,openai_tts_1"
    assert properties["asr"] == {"vendor": "deepgram"}
    assert properties["llm"] == {"vendor": "openai"}
    assert properties["tts"] == {"vendor": "openai", "params": {"voice": "alloy"}}


def test_resolve_session_presets_minimax_and_explicit_precedence():
    preset, properties = resolve_session_presets(
        "deepgram_nova_2",
        {
            "asr": {"vendor": "deepgram", "params": {"model": "nova-3"}},
            "tts": {"vendor": "minimax", "params": {"model": "speech-2.8-turbo"}},
        },
    )
    assert preset == "deepgram_nova_2,minimax_speech_2_8_turbo"
    assert properties["asr"]["params"] == {"model": "nova-3"}
    assert properties["tts"] == {"vendor": "minimax"}


def test_resolve_session_presets_skips_inference_when_credentials_or_nonstandard_values_present():
    assert resolve_session_presets(
        None, {"asr": {"vendor": "deepgram", "params": {"model": "nova-3", "api_key": "key"}}}
    )[0] is None
    assert resolve_session_presets(
        None,
        {
            "llm": {
                "vendor": "openai",
                "url": "https://example.com/chat/completions",
                "params": {"model": "gpt-5-mini"},
            }
        },
    )[0] is None
    assert resolve_session_presets(
        None, {"tts": {"vendor": "minimax", "params": {"model": "speech-2.8-turbo", "key": "secret"}}}
    )[0] is None
