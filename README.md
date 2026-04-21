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

Minimal builder-based example using supported preset-backed models with no vendor API keys:

```python
from agora_agent import Agora, Area
from agora_agent.agentkit import Agent, DeepgramSTT, OpenAI, OpenAITTS

def main() -> None:
    client = Agora(
        area=Area.US,
        app_id="your-app-id",
        app_certificate="your-app-certificate",
    )

    agent = Agent(
        instructions="You are a concise voice assistant.",
        greeting="Hello! How can I help you today?",
    ).with_stt(
        DeepgramSTT(model="nova-3")
    ).with_llm(
        OpenAI(model="gpt-5-mini")
    ).with_tts(
        OpenAITTS(voice="alloy")
    )

    session = agent.create_session(
        client,
        channel="support-room-123",
        agent_uid="1",
        remote_uids=["100"],
    )

    agent_id = session.start()
    print(agent_id)


if __name__ == "__main__":
    main()
```

### Why no token or vendor key in the example?

The SDK-managed path is the recommended path. `Agora` generates the required ConvoAI REST auth and RTC join tokens automatically, and AgentKit infers the matching supported presets from the vendor configs when you omit vendor API keys.

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
