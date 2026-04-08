---
sidebar_position: 3
title: Quick Start
description: Build and run your first Agora Conversational AI agent in Python with app credentials and presets.
---

# Quick Start

This guide uses the recommended onboarding path:

- `app_id`, `app_certificate`, and `area` on `Agora` or `AsyncAgora`
- `preset` for Agora-managed ASR, LLM, and TTS
- automatic ConvoAI REST auth and RTC join token generation
- no vendor API keys in application code

## Sync example

```python
from agora_agent import Agora, Area
from agora_agent.agentkit import Agent, AgentPresets


def main() -> None:
    client = Agora(
        area=Area.US,
        app_id="your-app-id",
        app_certificate="your-app-certificate",
    )

    # Agent-level behavior lives here. Vendor selection comes from presets below.
    agent = Agent(
        name="support-assistant",
        instructions="You are a concise support voice assistant.",
        greeting="Hello! How can I help you today?",
        max_history=10,
    )

    session = agent.create_session(
        client,
        channel="support-room-123",
        agent_uid="1",
        remote_uids=["100"],
        idle_timeout=120,
        preset=[
            AgentPresets.asr.deepgram_nova_3,
            AgentPresets.llm.openai_gpt_5_mini,
            AgentPresets.tts.openai_tts_1,
        ],
    )

    agent_session_id = session.start()
    print(f"Agent started: {agent_session_id}")

    session.say("Thanks for calling Agora support.")
    session.stop()


if __name__ == "__main__":
    main()
```

## What this does

1. `Agora` runs in app-credentials mode when you pass `app_id` and `app_certificate` only.
2. `Agent` holds reusable behavior such as instructions, greeting, and history settings.
3. `preset` tells Agora which managed ASR, LLM, and TTS vendors to run.
4. `session.start()` lets the SDK generate the required auth tokens automatically.
5. `session.start()` returns the unique agent session ID.

## Async applications

For `asyncio` services, switch to `AsyncAgora` and `await` the session methods. The preset and token-auth flow stays the same.

## When to use BYOK instead

Use presets when you want the fastest path to a working agent.

Use BYOK when you need to:

- supply your own vendor API keys
- use models outside the preset catalog
- point at custom vendor endpoints
- manage vendor-specific parameters directly

See [BYOK Guide](../guides/byok.md).

## Next steps

- [Authentication](./authentication.md)
- [BYOK Guide](../guides/byok.md)
- [MLLM Flow](../guides/mllm-flow.md)
- [Agent Reference](../reference/agent.md)
