# Agora Conversational AI Python SDK

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2FAgoraIO-Conversational-AI%2Fagora-agent-python-sdk)
[![pypi](https://img.shields.io/pypi/v/agora-agent-sdk)](https://pypi.python.org/pypi/agora-agent-sdk)

The Agora Conversational AI SDK provides convenient access to the Agora Conversational AI APIs, enabling you to build voice-powered AI agents with support for both **cascading flows** (ASR → LLM → TTS) and **multimodal flows** (MLLM) for real-time audio processing.

## Installation

```sh
pip install agora-agent-sdk
```

## Quick Start

Use the **builder pattern** with `Agent` and `AgentSession`. The SDK auto-generates all required tokens:

```python
from agora_agent import Agora, Area
from agora_agent.agentkit import Agent, expires_in_hours
from agora_agent.agentkit.vendors import OpenAI, ElevenLabsTTS, DeepgramSTT

client = Agora(
    area=Area.US,
    app_id="your-app-id",
    app_certificate="your-app-certificate",
)

agent = (
    Agent(name="support-assistant", instructions="You are a helpful voice assistant.")
    # Create Agent: STT → LLM → TTS → (optional) Avatar
    .with_stt(DeepgramSTT(api_key="your-deepgram-key", language="en-US"))
    .with_llm(OpenAI(api_key="your-openai-key", model="gpt-4o-mini"))
    .with_tts(ElevenLabsTTS(key="your-elevenlabs-key", model_id="eleven_flash_v2_5", voice_id="your-voice-id", sample_rate=24000))
    # .with_avatar(HeyGenAvatar(...))  # optional
)

session = agent.create_session(
    client,
    channel="support-room-123",
    agent_uid="1",
    remote_uids=["100"],
    expires_in=expires_in_hours(12),  # optional — default is 24 h (Agora max)
)

# start() returns a session ID unique to this agent session
agent_session_id = session.start()

# In production, stop is typically called when your client signals the session has ended.
# Your server receives that request and calls session.stop().
session.stop()
```

For async usage, use `AsyncAgora` and `await session.start()`, etc. See [Quick Start](docs/getting-started/quick-start.md).

### Session lifecycle

`start()` joins the agent to the channel and returns a **session ID** — a unique identifier for this agent session. The session stays active until `stop()` is called.

There are two ways to stop a session depending on how your server is structured:

**Option 1 — Hold the session in memory:**

```python
# start-session handler
agent_session_id = session.start()  # unique ID for this session
# stop-session handler (same process, session still in scope)
session.stop()
```

**Option 2 — Store the session ID and stop by ID (stateless servers):**

```python
# start-session handler: return session ID to your client app
agent_session_id = session.start()
# ... return agent_session_id to client ...

# stop-session handler: client sends back agent_session_id
client = Agora(area=Area.US, app_id="...", app_certificate="...")
client.stop_agent(agent_session_id)
```

### Manual tokens (for debugging)

Generate tokens yourself and pass them in — useful when inspecting or reusing tokens:

```python
from agora_agent import Agora, Area
from agora_agent.agentkit.token import generate_convo_ai_token, expires_in_hours

APP_ID = "your-app-id"
APP_CERT = "your-app-certificate"
CHANNEL = "support-room-123"
AGENT_UID = "1"

# Auth header token — used by the SDK to authenticate REST API calls
auth_token = generate_convo_ai_token(
    app_id=APP_ID, app_certificate=APP_CERT,
    channel_name=CHANNEL, account=AGENT_UID,
    token_expire=expires_in_hours(12),
)

# Channel join token — embedded in the start request so the agent can join the channel
join_token = generate_convo_ai_token(
    app_id=APP_ID, app_certificate=APP_CERT,
    channel_name=CHANNEL, account=AGENT_UID,
    token_expire=expires_in_hours(12),
)

client = Agora(
    area=Area.US,
    app_id=APP_ID,
    app_certificate=APP_CERT,
    auth_token=auth_token,  # SDK sets Authorization: agora token=<auth_token>
)

session = agent.create_session(
    client, channel=CHANNEL, agent_uid=AGENT_UID, remote_uids=["100"],
    token=join_token,  # channel join token
)
```

## Documentation

| Topic              | Link                                                                             |
| ------------------ | -------------------------------------------------------------------------------- |
| **API docs**       | [docs.agora.io](https://docs.agora.io/en/conversational-ai/overview)             |
| **Installation**   | [docs/getting-started/installation.md](docs/getting-started/installation.md)     |
| **Authentication** | [docs/getting-started/authentication.md](docs/getting-started/authentication.md) |
| **Quick Start**    | [docs/getting-started/quick-start.md](docs/getting-started/quick-start.md)       |
| **Cascading flow** | [docs/guides/cascading-flow.md](docs/guides/cascading-flow.md)                   |
| **MLLM flow**      | [docs/guides/mllm-flow.md](docs/guides/mllm-flow.md)                             |
| **Low-level API**  | [docs/guides/low-level-api.md](docs/guides/low-level-api.md)                     |
| **Error handling** | [docs/guides/error-handling.md](docs/guides/error-handling.md)                   |
| **Pagination**     | [docs/guides/pagination.md](docs/guides/pagination.md)                           |
| **Advanced**       | [docs/guides/advanced.md](docs/guides/advanced.md)                               |
| **API reference**  | [reference.md](reference.md)                                                     |

## Contributing

This library is generated programmatically. Contributions to the README and docs are welcome. For code changes, open an issue first to discuss.
