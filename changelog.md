# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [v1.2.0] — 2026-03-27

### Fixed

- **`AresSTT`** — Removed redundant `language` key from the `params` dict. Language is now emitted only at the top level. `params` is only included when `additional_params` is provided.
- **`OpenAIRealtime` / `VertexAI` (MLLM)** — Agent-level `greeting`, `failure_message`, and `max_history` overrides are now correctly applied when the agent is in MLLM mode. Previously these values were silently dropped.

### Changed

- **`OpenAITTS`** — Renamed constructor parameter `key` → `api_key` to match the Agora server API expectation. ⚠️ **Breaking change.**
- **`CartesiaTTS`** — Renamed constructor parameter `key` → `api_key`. Voice is now serialized as `{"mode": "id", "id": "<voice_id>"}` instead of a flat `voice_id` string. ⚠️ **Breaking change.**
- **`HeyGenAvatar`** — Removed legacy fields `avatar_name`, `voice_id`, `language`, `version`. Added `agora_token`, `avatar_id`, `enable`, `disable_idle_timeout`, `activity_idle_timeout`. The config now includes a top-level `enable` field (defaults `true`). ⚠️ **Breaking change.**

### Added

- **`OpenAITTS`** — New optional parameters: `response_format` (str, e.g. `"pcm"`) and `speed` (float).
- **`CartesiaTTS`** — `voice_id` user-facing field is preserved; voice is serialized to the required nested object format automatically.
- **`RimeTTS`** — New optional parameters: `lang` (str), `sampling_rate` (int, serialized as `samplingRate`), `speed_alpha` (float, serialized as `speedAlpha`).
- **`OpenAIRealtime`** — New optional parameters: `predefined_tools` (List[str]), `failure_message` (str), `max_history` (int).
- **`VertexAI` (MLLM)** — New optional parameters: `predefined_tools` (List[str]), `failure_message` (str), `max_history` (int).
- **`HeyGenAvatar`** — New fields: `agora_token` (str, optional), `avatar_id` (str, optional), `enable` (bool, optional, default `True`), `disable_idle_timeout` (bool, optional), `activity_idle_timeout` (int, optional).

## [v1.1.0] — 2026-03-17

### Added

- `MurfTTS` vendor


### Fixed

- `MiniMaxTTS`: added required `group_id`, `url`, and correctly nested `voice_setting.voice_id` — previously missing, requiring users to bypass the SDK entirely
- `SarvamTTS`: corrected schema to `key` + `speaker` + `target_language_code` (was incorrectly using `api_key`, `voice_id`, `model`)
- All LLM vendors: added `max_history` field for conversation history caching
- `AzureOpenAI` LLM: added `params` escape hatch for passing arbitrary API parameters
- `Anthropic` LLM: added `url` for custom endpoints and `params` escape hatch
- `Gemini` LLM: added `url` for custom endpoints and `params` escape hatch; named model params (`temperature`, `top_p`, `top_k`, `max_output_tokens`) now take precedence over `params` dict
- `SpeechmaticsSTT`, `SarvamSTT`: added optional `model` field

## [v1.0.0] — 2026-03-11

Initial stable release of the Agora Agent Server SDK for Python.

### Added

- `Agent` builder with fluent API (`.with_llm()`, `.with_tts()`, `.with_stt()`, `.with_mllm()`, `.with_avatar()`)
- `AgentSession` and `AsyncAgentSession` for synchronous and async session lifecycle management
- Automatic token generation — pass `app_id` + `app_certificate` and tokens are handled internally
- Token utilities: `generate_rtc_token`, `generate_convo_ai_token`, `expires_in_hours`, `expires_in_minutes`
- Turn detection configuration via `TurnDetectionConfig` with nested `StartOfSpeechConfig` and `EndOfSpeechConfig`
- SAL (Selective Attention Locking) via `SalConfig` with `SalMode`
- Filler words support: `FillerWordsConfig`, `FillerWordsTrigger`, `FillerWordsContent`
- Session parameters: `SessionParams`, `SilenceConfig`, `FarewellConfig`, `ParametersDataChannel`
- Geofencing via `GeofenceConfig`
- Advanced features (MLLM mode) via `AdvancedFeatures`
- Type-safe constants: `DataChannel`, `SilenceActionValues`, `SalModeValues`, `GeofenceArea`, `FillerWordsSelectionRule`, `TurnDetectionTypeValues`
- Vendor integrations:
  - **LLM**: `OpenAI`, `AzureOpenAI`, `Anthropic`, `Gemini`, `VertexAI`
  - **MLLM**: `OpenAIRealtime`
  - **TTS**: `ElevenLabsTTS`, `MicrosoftTTS`, `OpenAITTS`, `CartesiaTTS`, `GoogleTTS`, `AmazonTTS`, `HumeAITTS`, `RimeTTS`, `FishAudioTTS`, `MiniMaxTTS`, `SarvamTTS`
  - **STT**: `DeepgramSTT`, `MicrosoftSTT`, `OpenAISTT`, `GoogleSTT`, `AmazonSTT`, `AssemblyAISTT`, `AresSTT`, `SarvamSTT`, `SpeechmaticsSTT`
  - **Avatar**: `HeyGenAvatar`, `AkoolAvatar`
