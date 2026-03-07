---
sidebar_position: 2
title: Agent
description: Full API reference for the Python Agent builder class.
---

# Agent Reference

**Import:** `from agora_agent.agentkit import Agent` or `from agora_agent import Agent`

## Constructor

```python
Agent(
    name: Optional[str] = None,
    instructions: Optional[str] = None,
    turn_detection: Optional[TurnDetectionConfig] = None,
    sal: Optional[SalConfig] = None,
    advanced_features: Optional[Dict[str, Any]] = None,
    parameters: Optional[SessionParams] = None,
    greeting: Optional[str] = None,
    failure_message: Optional[str] = None,
    max_history: Optional[int] = None,
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `Optional[str]` | `None` | Agent name, used as default session name |
| `instructions` | `Optional[str]` | `None` | System prompt for the LLM |
| `turn_detection` | `Optional[TurnDetectionConfig]` | `None` | Turn detection configuration |
| `sal` | `Optional[SalConfig]` | `None` | Speech Activity Level configuration |
| `advanced_features` | `Optional[Dict[str, Any]]` | `None` | Advanced features dict (e.g., `{'enable_mllm': True}`) |
| `parameters` | `Optional[SessionParams]` | `None` | Additional session parameters |
| `greeting` | `Optional[str]` | `None` | Auto-spoken greeting when agent joins |
| `failure_message` | `Optional[str]` | `None` | Spoken on error |
| `max_history` | `Optional[int]` | `None` | Max conversation history length |

## Builder Methods

All builder methods return a new `Agent` instance (immutable pattern).

### `with_llm(vendor: BaseLLM) -> Agent`

Set the LLM vendor for cascading flow.

```python
from agora_agent.agentkit.vendors import OpenAI
agent = Agent().with_llm(OpenAI(api_key='your-key', model='gpt-4o-mini'))
```

### `with_tts(vendor: BaseTTS) -> Agent`

Set the TTS vendor. Records the vendor's `sample_rate` for avatar validation.

```python
from agora_agent.agentkit.vendors import ElevenLabsTTS
agent = Agent().with_tts(ElevenLabsTTS(key='your-key', model_id='eleven_flash_v2_5', voice_id='your-voice-id'))
```

### `with_stt(vendor: BaseSTT) -> Agent`

Set the STT (ASR) vendor.

```python
from agora_agent.agentkit.vendors import DeepgramSTT
agent = Agent().with_stt(DeepgramSTT(api_key='your-key', language='en-US'))
```

### `with_mllm(vendor: BaseMLLM) -> Agent`

Set the MLLM vendor for multimodal flow. Requires `advanced_features={'enable_mllm': True}`.

```python
from agora_agent.agentkit.vendors import OpenAIRealtime
agent = Agent(advanced_features={'enable_mllm': True}).with_mllm(OpenAIRealtime(api_key='your-key'))
```

### `with_avatar(vendor: BaseAvatar) -> Agent`

Set the avatar vendor. Raises `ValueError` if TTS sample rate does not match the avatar's `required_sample_rate`.

```python
from agora_agent.agentkit.vendors import HeyGenAvatar
agent = agent.with_avatar(HeyGenAvatar(api_key='your-key', quality='medium', agora_uid='2'))
```

**Raises:** `ValueError` — `"Avatar requires TTS sample rate of {required} Hz, but TTS is configured with {actual} Hz. Please update your TTS sample_rate to {required}."`

### `with_turn_detection(config: TurnDetectionConfig) -> Agent`

Override turn detection settings.

### `with_instructions(instructions: str) -> Agent`

Override the system prompt.

### `with_greeting(greeting: str) -> Agent`

Override the greeting message.

### `with_name(name: str) -> Agent`

Override the agent name.

## `create_session()`

```python
create_session(
    client: Any,
    channel: str,
    agent_uid: str,
    remote_uids: List[str],
    name: Optional[str] = None,
    token: Optional[str] = None,
    idle_timeout: Optional[int] = None,
    enable_string_uid: Optional[bool] = None,
) -> AgentSession
```

Creates an `AgentSession` bound to the given client and channel.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `client` | `Agora` or `AsyncAgora` | Yes | Authenticated client |
| `channel` | `str` | Yes | Channel name |
| `agent_uid` | `str` | Yes | UID for the agent |
| `remote_uids` | `List[str]` | Yes | UIDs of remote participants |
| `name` | `Optional[str]` | No | Session name (defaults to agent name) |
| `token` | `Optional[str]` | No | Pre-built RTC token |
| `idle_timeout` | `Optional[int]` | No | Idle timeout in seconds |
| `enable_string_uid` | `Optional[bool]` | No | Enable string UIDs |

**Returns:** `AgentSession`

## `to_properties()`

Converts the agent configuration into a `StartAgentsRequestProperties` object for the Agora API. Called internally by `AgentSession.start()`.

```python
to_properties(
    channel: str,
    agent_uid: str,
    remote_uids: List[str],
    idle_timeout: Optional[int] = None,
    enable_string_uid: Optional[bool] = None,
    token: Optional[str] = None,
    app_id: Optional[str] = None,
    app_certificate: Optional[str] = None,
    token_expiry_seconds: Optional[int] = None,
) -> StartAgentsRequestProperties
```

**Raises:** `ValueError` if neither `token` nor `app_id`+`app_certificate` is provided, or if required vendors (LLM, TTS) are missing in cascading mode.

## Properties

| Property | Type | Description |
|---|---|---|
| `name` | `Optional[str]` | Agent name |
| `instructions` | `Optional[str]` | System prompt |
| `greeting` | `Optional[str]` | Greeting message |
| `llm` | `Optional[Dict[str, Any]]` | LLM config dict (from `to_config()`) |
| `tts` | `Optional[Dict[str, Any]]` | TTS config dict |
| `stt` | `Optional[Dict[str, Any]]` | STT config dict |
| `mllm` | `Optional[Dict[str, Any]]` | MLLM config dict |
| `turn_detection` | `Optional[TurnDetectionConfig]` | Turn detection settings |
| `config` | `Dict[str, Any]` | Full configuration dict |
