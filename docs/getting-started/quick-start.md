---
sidebar_position: 3
title: Quick Start
description: Build and run your first Agora Conversational AI agent in Python.
---

# Quick Start

This guide walks you through building a voice agent using the cascading flow (ASR → LLM → TTS) with both sync and async clients.

## Sync Example

This complete script creates an agent with OpenAI for the LLM, ElevenLabs for TTS, and Deepgram for STT:

```python
from agora_agent import Agora, Area
from agora_agent.agentkit import Agent
from agora_agent.agentkit.vendors import OpenAI, ElevenLabsTTS, DeepgramSTT

# 1. Create a client with app credentials
client = Agora(
    area=Area.US,
    app_id='your-app-id',
    app_certificate='your-app-certificate',
)

# 2. Build an agent with vendor configuration
agent = (
    Agent(name='support-assistant', instructions='You are a helpful voice assistant.')
    .with_llm(OpenAI(api_key='your-openai-key', model='gpt-4o-mini'))
    .with_tts(ElevenLabsTTS(key='your-elevenlabs-key', model_id='eleven_flash_v2_5', voice_id='your-voice-id'))
    .with_stt(DeepgramSTT(api_key='your-deepgram-key', language='en-US'))
)

# 3. Create and start a session
session = agent.create_session(
    client,
    channel='support-room-123',
    agent_uid='1',
    remote_uids=['100'],
)
agent_id = session.start()
print(f'Agent started with ID: {agent_id}')

# 4. Interact with the agent
session.say('Hello! How can I help you today?')

# 5. Stop the session when done
session.stop()
print('Agent stopped.')
```

## Async Example

For async applications, use `AsyncAgora` for the client. All session methods become coroutines that require `await`:

```python
import asyncio
from agora_agent import AsyncAgora, Area
from agora_agent.agentkit import Agent
from agora_agent.agentkit.vendors import OpenAI, ElevenLabsTTS, DeepgramSTT

async def main():
    # 1. Create an async client
    client = AsyncAgora(
        area=Area.US,
        app_id='your-app-id',
        app_certificate='your-app-certificate',
    )

    # 2. Build an agent (same as sync — Agent is client-agnostic)
    agent = (
        Agent(name='support-assistant', instructions='You are a helpful voice assistant.')
        .with_llm(OpenAI(api_key='your-openai-key', model='gpt-4o-mini'))
        .with_tts(ElevenLabsTTS(key='your-elevenlabs-key', model_id='eleven_flash_v2_5', voice_id='your-voice-id'))
        .with_stt(DeepgramSTT(api_key='your-deepgram-key', language='en-US'))
    )

    # 3. Create a session — works with both sync and async clients
    session = agent.create_session(
        client,
        channel='support-room-123',
        agent_uid='1',
        remote_uids=['100'],
    )

    # 4. All session methods are coroutines — use await
    agent_id = await session.start()
    print(f'Agent started with ID: {agent_id}')

    await session.say('Hello! How can I help you today?')
    await session.stop()
    print('Agent stopped.')

asyncio.run(main())
```

## What Happens Under the Hood

1. The `Agent` builder collects your vendor configuration into a properties object
2. `session.start()` generates an RTC token (using the client's `app_id` and `app_certificate`), then calls the Agora API to start the agent
3. The agent connects to the specified channel and begins listening for audio from the remote UIDs
4. `session.say()` sends text to be spoken by the agent's TTS
5. `session.stop()` gracefully shuts down the agent

## Next Steps

- Learn how the [Agent builder](../concepts/agent.md) works
- Understand the [AgentSession lifecycle](../concepts/session.md)
- Explore the full [vendor catalog](../concepts/vendors.md)
- Try the [MLLM flow](../guides/mllm-flow.md) for multimodal agents
