---
sidebar_position: 3
title: Avatar Integration
description: Add a digital avatar (HeyGen or Akool) to your Conversational AI agent.
---

# Avatar Integration

You can attach a digital avatar to your voice agent so that users see a visual representation of the AI speaking. Two avatar providers are supported:

| Provider | Class | Required TTS Sample Rate |
|---|---|---|
| HeyGen | `HeyGenAvatar` | 24000 Hz |
| Akool | `AkoolAvatar` | 16000 Hz |

## Sample Rate Constraint

Each avatar vendor requires a specific TTS sample rate. The SDK validates this when you call `with_avatar()` — if the TTS sample rate does not match, a `ValueError` is raised immediately:

```
ValueError: Avatar requires TTS sample rate of 24000 Hz, but TTS is configured with 16000 Hz. Please update your TTS sample_rate to 24000.
```

This validation happens at build time (when chaining methods), not at runtime when the session starts. Python raises this as a `ValueError` — there is no compile-time check as in statically typed languages.

Additionally, if the TTS `sample_rate` is not explicitly set (returns `None`), the SDK issues a warning:

```
UserWarning: Avatar requires TTS sample rate of 24000 Hz, but TTS sample_rate is not explicitly set. Please ensure your TTS provider is configured for 24000 Hz.
```

## HeyGen Avatar (24 kHz)

HeyGen requires a TTS vendor configured at 24000 Hz:

```python
from agora_agent import Agora, Area
from agora_agent.agentkit import Agent
from agora_agent.agentkit.vendors import OpenAI, ElevenLabsTTS, DeepgramSTT, HeyGenAvatar

client = Agora(
    area=Area.US,
    app_id='your-app-id',
    app_certificate='your-app-certificate',
)

agent = (
    Agent(name='avatar-agent', instructions='You are a helpful assistant with a visual avatar.')
    .with_llm(OpenAI(api_key='your-openai-key', model='gpt-4o-mini'))
    .with_tts(ElevenLabsTTS(
        key='your-elevenlabs-key',
        model_id='eleven_flash_v2_5',
        voice_id='your-voice-id',
        sample_rate=24000,  # Must be 24000 for HeyGen
    ))
    .with_stt(DeepgramSTT(api_key='your-deepgram-key', language='en-US'))
    .with_avatar(HeyGenAvatar(
        api_key='your-heygen-key',
        quality='medium',
        agora_uid='2',
        avatar_name='your-avatar-name',
    ))
)

session = agent.create_session(client, channel='avatar-room', agent_uid='1', remote_uids=['100'])
agent_id = session.start()
session.say('Hello! I am your visual assistant.')
session.stop()
```

## Akool Avatar (16 kHz)

Akool requires a TTS vendor configured at 16000 Hz:

```python
from agora_agent.agentkit.vendors import ElevenLabsTTS, AkoolAvatar

agent = (
    Agent(name='akool-agent', instructions='You are a helpful assistant.')
    .with_llm(OpenAI(api_key='your-openai-key', model='gpt-4o-mini'))
    .with_tts(ElevenLabsTTS(
        key='your-elevenlabs-key',
        model_id='eleven_flash_v2_5',
        voice_id='your-voice-id',
        sample_rate=16000,  # Must be 16000 for Akool
    ))
    .with_stt(DeepgramSTT(api_key='your-deepgram-key', language='en-US'))
    .with_avatar(AkoolAvatar(
        api_key='your-akool-key',
        agora_uid='2',
        avatar_id='your-avatar-id',
    ))
)
```

## Common Mistake: Wrong Sample Rate

This example shows what happens when the TTS sample rate does not match the avatar's requirement:

```python
# This raises ValueError at build time
agent = (
    Agent(name='broken-agent', instructions='You are a helpful assistant.')
    .with_llm(OpenAI(api_key='your-openai-key', model='gpt-4o-mini'))
    .with_tts(ElevenLabsTTS(
        key='your-elevenlabs-key',
        model_id='eleven_flash_v2_5',
        voice_id='your-voice-id',
        sample_rate=16000,  # 16 kHz
    ))
    .with_stt(DeepgramSTT(api_key='your-deepgram-key', language='en-US'))
    .with_avatar(HeyGenAvatar(  # Requires 24 kHz — mismatch!
        api_key='your-heygen-key',
        quality='medium',
        agora_uid='2',
    ))
)
# ValueError: Avatar requires TTS sample rate of 24000 Hz, but TTS is configured
# with 16000 Hz. Please update your TTS sample_rate to 24000.
```

**Fix:** Change `sample_rate=16000` to `sample_rate=24000` on the TTS vendor.

## Order Matters

The `with_avatar()` call validates against the currently configured TTS. Always call `with_tts()` before `with_avatar()`:

```python
# Correct order: TTS first, then avatar
agent = (
    Agent(name='my-agent', instructions='You are helpful.')
    .with_tts(ElevenLabsTTS(key='your-elevenlabs-key', model_id='eleven_flash_v2_5', voice_id='your-voice-id', sample_rate=24000))
    .with_avatar(HeyGenAvatar(api_key='your-heygen-key', quality='medium', agora_uid='2'))
)
```

If you call `with_avatar()` before `with_tts()`, the sample rate check is deferred to `session.start()`, which validates the configuration before making the API call.

## HeyGen Options

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | `str` | Yes | HeyGen API key |
| `quality` | `str` | Yes | Avatar quality: `low`, `medium`, or `high` |
| `agora_uid` | `str` | Yes | Agora UID for the avatar video stream |
| `avatar_name` | `str` | No | Avatar name |
| `voice_id` | `str` | No | Voice ID |
| `language` | `str` | No | Language code |
| `version` | `str` | No | API version (`v1` or `v2`) |

## Akool Options

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | `str` | Yes | Akool API key |
| `agora_uid` | `str` | Yes | Agora UID for the avatar video stream |
| `avatar_id` | `str` | No | Avatar ID |
