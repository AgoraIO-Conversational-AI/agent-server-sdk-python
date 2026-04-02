import pytest

from agora_agent.agentkit import (
    AnamAvatar,
    GeminiLive,
    LiveAvatarAvatar,
    validate_avatar_config,
    validate_tts_sample_rate,
)
from agora_agent.agentkit.vendors import (
    AmazonSTT,
    AmazonTTS,
    Anthropic,
    AresSTT,
    AssemblyAISTT,
    AzureOpenAI,
    CartesiaTTS,
    DeepgramSTT,
    ElevenLabsTTS,
    FishAudioTTS,
    Gemini,
    GoogleSTT,
    GoogleTTS,
    HeyGenAvatar,
    HumeAITTS,
    MicrosoftSTT,
    MicrosoftTTS,
    MiniMaxTTS,
    MurfTTS,
    OpenAI,
    OpenAIRealtime,
    OpenAISTT,
    OpenAITTS,
    RimeTTS,
    SarvamSTT,
    SarvamTTS,
    SpeechmaticsSTT,
    VertexAI,
)


def test_llm_vendor_mappings_cover_core_shapes_and_defaults():
    assert OpenAI(api_key="key", model="gpt-4o-mini").to_config()["url"] == "https://api.openai.com/v1/chat/completions"
    assert "api_key" not in OpenAI(model="gpt-5-mini").to_config()
    assert "params" not in AzureOpenAI(
        api_key="key",
        endpoint="https://azure.example.com",
        deployment_name="deploy",
    ).to_config()
    anthropic = Anthropic(api_key="key", model="claude", temperature=0.3, top_p=0.7).to_config()
    assert anthropic["params"]["temperature"] == 0.3
    assert anthropic["params"]["top_p"] == 0.7
    gemini = Gemini(api_key="key", model="gemini", temperature=0.2, top_p=0.8, top_k=10).to_config()
    assert gemini["style"] == "gemini"
    assert gemini["params"]["top_k"] == 10


def test_mllm_vendor_mappings_cover_optional_branches():
    realtime = OpenAIRealtime(api_key="key").to_config()
    assert realtime == {"vendor": "openai", "style": "openai", "api_key": "key"}

    vertex = VertexAI(
        model="gemini-live",
        project_id="project",
        location="us-central1",
        adc_credentials_string="creds",
        additional_params={"temperature": 0.2},
    ).to_config()
    assert vertex["vendor"] == "vertexai"
    assert vertex["params"]["temperature"] == 0.2

    gemini_live = GeminiLive(api_key="key", model="gemini-live", voice="Aoede").to_config()
    assert gemini_live["vendor"] == "gemini"
    assert gemini_live["params"]["voice"] == "Aoede"


def test_stt_vendor_mappings_cover_all_wrappers():
    assert SpeechmaticsSTT(api_key="key", language="en").to_config()["vendor"] == "speechmatics"
    assert DeepgramSTT(api_key="key", model="nova-3", smart_format=True, punctuation=True).to_config()["params"][
        "smart_format"
    ]
    assert MicrosoftSTT(key="key", region="eastus").to_config()["vendor"] == "microsoft"
    assert OpenAISTT(api_key="key", model="whisper-1").to_config()["vendor"] == "openai"
    assert GoogleSTT(api_key="key", language="en-US").to_config()["vendor"] == "google"
    assert AmazonSTT(access_key="a", secret_key="b", region="us-east-1").to_config()["vendor"] == "amazon"
    assert AssemblyAISTT(api_key="key").to_config()["vendor"] == "assemblyai"
    assert AresSTT(language="en").to_config()["vendor"] == "ares"
    assert SarvamSTT(api_key="key", language="en").to_config()["vendor"] == "sarvam"


def test_tts_vendor_mappings_cover_all_wrappers_and_skip_patterns():
    assert ElevenLabsTTS(key="key", model_id="model", voice_id="voice", skip_patterns=[1]).to_config()["skip_patterns"] == [1]
    assert MicrosoftTTS(key="key", region="eastus", voice_name="voice").to_config()["vendor"] == "microsoft"
    assert OpenAITTS(voice="alloy").to_config()["params"] == {"voice": "alloy"}
    assert CartesiaTTS(api_key="key", voice_id="voice").to_config()["params"]["voice"]["id"] == "voice"
    assert GoogleTTS(key="key", voice_name="voice").to_config()["vendor"] == "google"
    assert AmazonTTS(access_key="a", secret_key="b", region="us-east-1", voice_id="voice").to_config()["vendor"] == "amazon"
    assert HumeAITTS(key="key").to_config()["vendor"] == "humeai"
    assert RimeTTS(key="key", speaker="speaker").to_config()["vendor"] == "rime"
    assert FishAudioTTS(key="key", reference_id="ref").to_config()["vendor"] == "fishaudio"
    assert MiniMaxTTS(model="speech-2.8-turbo").to_config()["params"] == {"model": "speech-2.8-turbo"}
    assert SarvamTTS(key="key", speaker="speaker", target_language_code="en-IN").to_config()["vendor"] == "sarvam"
    assert MurfTTS(key="key", voice_id="voice").to_config()["vendor"] == "murf"


def test_avatar_vendor_mappings_and_validators_cover_failure_branches():
    with pytest.raises(ValueError, match="quality"):
        HeyGenAvatar(api_key="key", quality="bad", agora_uid="1")

    liveavatar = LiveAvatarAvatar(
        api_key="key",
        quality="high",
        agora_uid="1",
        avatar_id="avatar",
        disable_idle_timeout=True,
        activity_idle_timeout=30,
    ).to_config()
    assert liveavatar["vendor"] == "liveavatar"
    validate_avatar_config(liveavatar)

    anam = AnamAvatar(api_key="key", persona_id="persona").to_config()
    assert anam["vendor"] == "anam"
    validate_avatar_config(anam)

    with pytest.raises(ValueError, match="HeyGen"):
        validate_tts_sample_rate(HeyGenAvatar(api_key="key", quality="high", agora_uid="1").to_config(), 16000)
