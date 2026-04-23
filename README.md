# Agora Agent Server SDK for Python

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2FAgoraIO-Conversational-AI%2Fagent-server-sdk-python)
[![pypi](https://img.shields.io/pypi/v/agora-agent-server-sdk)](https://pypi.python.org/pypi/agora-agent-server-sdk)

The Agora Conversational AI SDK provides convenient access to the Agora Conversational AI APIs, enabling you to build voice-powered AI agents with support for both cascading flows (ASR -> LLM -> TTS) and multimodal flows (MLLM) for real-time audio processing.

## Requirements

- Python 3.8+

## Installation

```sh
pip install agora-agent-server-sdk
```

## Quick Start

The recommended onboarding path is a server-side builder flow: define the agent once, configure preset-backed providers in the builder, and let AgentKit infer the reseller `preset` values when the session starts.

```python
import os
import time

from agora_agent import Agora, Area
from agora_agent.agentkit import (
    Agent,
    DataChannel,
    DeepgramSTT,
    MiniMaxTTS,
    OpenAI,
    expires_in_hours,
)

AGENT_PROMPT = (
    "You are a concise, technically credible voice assistant. "
    "Keep replies short unless the user asks for detail."
)

GREETING = "Hi there! I am your Agora voice assistant. How can I help?"


def start_conversation() -> str:
    app_id = os.environ["AGORA_APP_ID"]
    app_certificate = os.environ["AGORA_APP_CERTIFICATE"]

    client = Agora(
        area=Area.US,
        app_id=app_id,
        app_certificate=app_certificate,
    )

    agent = Agent(
        name=f"conversation-{int(time.time())}",
        instructions=AGENT_PROMPT,
        greeting=GREETING,
        failure_message="Please wait a moment.",
        max_history=50,
        turn_detection={
            "config": {
                "speech_threshold": 0.5,
                "start_of_speech": {
                    "mode": "vad",
                    "vad_config": {
                        "interrupt_duration_ms": 160,
                        "prefix_padding_ms": 300,
                    },
                },
                "end_of_speech": {
                    "mode": "vad",
                    "vad_config": {
                        "silence_duration_ms": 480,
                    },
                },
            },
        },
        advanced_features={
            "enable_rtm": True,
            "enable_tools": True,
        },
        parameters={
            "data_channel": DataChannel.RTM,
            "enable_error_message": True,
        },
    ).with_stt(
        DeepgramSTT(
            model="nova-3",
            language="en",
        )
    ).with_llm(
        OpenAI(
            model="gpt-4o-mini",
            greeting_message=GREETING,
            failure_message="Please wait a moment.",
            max_history=15,
            params={
                "max_tokens": 1024,
                "temperature": 0.7,
                "top_p": 0.95,
            },
        )
    ).with_tts(
        MiniMaxTTS(
            model="speech_2_6_turbo",
            voice_id="English_captivating_female1",
        )
    )

    session = agent.create_session(
        client,
        channel=f"demo-channel-{int(time.time())}",
        agent_uid="123456",
        remote_uids=["*"],
        idle_timeout=30,
        expires_in=expires_in_hours(1),
        debug=False,
    )

    return session.start()
```

### Why no token or vendor key in the example?

`Agora` generates the required ConvoAI REST auth and RTC join tokens automatically when you provide `app_id` and `app_certificate`. AgentKit then inspects the builder-provided vendor configs and infers the matching supported `preset` values for reseller-backed models, so you do not pass vendor API keys in this flow.

### BYOK version of the same builder flow

Use the same `Agent` builder shape, but provide credentials explicitly when you want vendor-managed billing and routing instead of Agora-managed presets.

```python
agent = Agent(
    instructions=AGENT_PROMPT,
    greeting=GREETING,
).with_stt(
    DeepgramSTT(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        model="nova-3",
        language="en",
    )
).with_llm(
    OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        model="gpt-4o-mini",
        max_tokens=1024,
        temperature=0.7,
        top_p=0.95,
    )
).with_tts(
    MiniMaxTTS(
        key=os.environ["MINIMAX_API_KEY"],
        group_id=os.environ["MINIMAX_GROUP_ID"],
        model="speech_2_6_turbo",
        voice_id="English_captivating_female1",
        url="wss://api-uw.minimax.io/ws/v1/t2a_v2",
    )
)
```

## BYOK

If you want to bring your own vendor credentials instead of using Agora-managed presets, use the BYOK guide:

- [BYOK Guide](./docs/guides/byok.md)

## Documentation

- [Overview](./docs/index.md)
- [Authentication](./docs/getting-started/authentication.md)
- [Quick Start](./docs/getting-started/quick-start.md)
- [BYOK Guide](./docs/guides/byok.md)
- [MLLM Flow](./docs/guides/mllm-flow.md)
- [Low-Level API](./docs/guides/low-level-api.md)

## Reference

- [SDK Reference](./reference.md)
- [Agora Conversational AI Docs](https://docs.agora.io/en/conversational-ai/overview)
