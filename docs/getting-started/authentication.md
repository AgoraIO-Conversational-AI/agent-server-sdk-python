---
sidebar_position: 2
title: Authentication
description: Configure the Python SDK with the recommended app-credentials flow and understand the supported auth modes.
---

# Authentication

The recommended production path is app credentials mode.

Create `Agora` or `AsyncAgora` with `app_id` and `app_certificate`, then let `AgentSession` generate the ConvoAI REST auth token and the RTC join token automatically.

## Recommended: app credentials

```python
from agora_agent import Agora, Area
from agora_agent.agentkit import Agent, AgentPresets

client = Agora(
    area=Area.US,
    app_id="your-app-id",
    app_certificate="your-app-certificate",
)

agent = Agent(instructions="Be concise.")

session = agent.create_session(
    client,
    channel="room-123",
    agent_uid="1",
    remote_uids=["100"],
    preset=[
        AgentPresets.asr.deepgram_nova_3,
        AgentPresets.llm.openai_gpt_5_mini,
        AgentPresets.tts.openai_tts_1,
    ],
)
```

## Why this is the default

- The SDK handles ConvoAI REST auth and RTC join token generation for you.
- Your onboarding code stays focused on agent behavior instead of auth plumbing.
- Your quick start code stays vendor-key free when you use presets.

## Other supported modes

The SDK also supports app-credentials mode and Basic Auth, but they are intentionally not the default onboarding path.

- App credentials are useful when your backend wants the SDK to mint ConvoAI REST tokens automatically.
- Basic Auth is supported for legacy integrations and account-level workflows.

## Inspecting the resolved auth mode

```python
print(client.auth_mode)  # "app-credentials"
```

## Other supported modes

`auth_token` and Basic Auth are still supported for advanced or legacy cases, but they are not the default onboarding path.
