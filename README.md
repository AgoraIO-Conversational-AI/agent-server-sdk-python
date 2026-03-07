# Agora Conversational AI Python SDK

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2FAgoraIO-Conversational-AI%2Fagora-agent-python-sdk)
[![pypi](https://img.shields.io/pypi/v/agora-agent-sdk)](https://pypi.python.org/pypi/agora-agent-sdk)

The Agora Conversational AI SDK provides convenient access to the Agora Conversational AI APIs, enabling you to build voice-powered AI agents with support for both **cascading flows** (ASR → LLM → TTS) and **multimodal flows** (MLLM) for real-time audio processing.

## Installation

```sh
pip install agora-agent-sdk
```

## Quick Start

Use the **builder pattern** with `Agent` and `AgentSession`:

```python
from agora_agent import Agora, Area
from agora_agent.agentkit import Agent
from agora_agent.agentkit.vendors import OpenAI, ElevenLabsTTS, DeepgramSTT

client = Agora(
    area=Area.US,
    app_id="your-app-id",
    app_certificate="your-app-certificate",
)

agent = (
    Agent(name="support-assistant", instructions="You are a helpful voice assistant.")
    .with_llm(OpenAI(api_key="your-openai-key", model="gpt-4o-mini"))
    .with_tts(ElevenLabsTTS(key="your-elevenlabs-key", model_id="eleven_flash_v2_5", voice_id="your-voice-id", sample_rate=24000))
    .with_stt(DeepgramSTT(api_key="your-deepgram-key", language="en-US"))
)

session = agent.create_session(client, channel="support-room-123", agent_uid="1", remote_uids=["100"])
agent_id = session.start()
session.say("Hello! How can I help you today?")
session.stop()
```

For async usage, use `AsyncAgora` and `await session.start()`, `await session.say()`, etc. See [Quick Start](docs/getting-started/quick-start.md).

## Documentation

| Topic | Link |
|-------|------|
| **API docs** | [docs.agora.io](https://docs.agora.io/en/conversational-ai/overview) |
| **Installation** | [docs/getting-started/installation.md](docs/getting-started/installation.md) |
| **Authentication** | [docs/getting-started/authentication.md](docs/getting-started/authentication.md) |
| **Quick Start** | [docs/getting-started/quick-start.md](docs/getting-started/quick-start.md) |
| **Cascading flow** | [docs/guides/cascading-flow.md](docs/guides/cascading-flow.md) |
| **MLLM flow** | [docs/guides/mllm-flow.md](docs/guides/mllm-flow.md) |
| **Low-level API** | [docs/guides/low-level-api.md](docs/guides/low-level-api.md) |
| **Error handling** | [docs/guides/error-handling.md](docs/guides/error-handling.md) |
| **Pagination** | [docs/guides/pagination.md](docs/guides/pagination.md) |
| **Advanced** | [docs/guides/advanced.md](docs/guides/advanced.md) |
| **API reference** | [reference.md](reference.md) |

## Contributing

This library is generated programmatically. Contributions to the README and docs are welcome. For code changes, open an issue first to discuss.
