---
sidebar_position: 4
title: BYOK
description: Bring your own vendor credentials and use custom vendor configuration with the Python SDK.
---

# BYOK

Use BYOK when you want to provide vendor credentials yourself instead of relying on Agora-managed presets.

Typical reasons:

- you need a vendor model that is not part of the preset catalog
- you want to point to a custom endpoint
- you want direct control over vendor-specific parameters
- your organization manages vendor billing separately from Agora

## Full example

```python
import os

from agora_agent import Agora, Area
from agora_agent.agentkit import Agent
from agora_agent.agentkit.vendors import DeepgramSTT, ElevenLabsTTS, OpenAI


def main() -> None:
    client = Agora(
        area=Area.US,
        app_id="your-app-id",
        app_certificate="your-app-certificate",
    )

    # In BYOK mode, each vendor carries its own credentials.
    agent = (
        Agent(
            name="support-assistant",
            instructions="You are a concise support voice assistant.",
            greeting="Hello! How can I help you today?",
            max_history=10,
        )
        .with_stt(
            DeepgramSTT(
                api_key=os.environ["DEEPGRAM_API_KEY"],
                model="nova-3",
                language="en-US",
            )
        )
        .with_llm(
            OpenAI(
                api_key=os.environ["OPENAI_API_KEY"],
                model="gpt-4o-mini",
            )
        )
        .with_tts(
            ElevenLabsTTS(
                key=os.environ["ELEVENLABS_API_KEY"],
                model_id="eleven_flash_v2_5",
                voice_id=os.environ["ELEVENLABS_VOICE_ID"],
                sample_rate=24000,
            )
        )
    )

    session = agent.create_session(
        client,
        channel="support-room-123",
        agent_uid="1",
        remote_uids=["100"],
        idle_timeout=120,
    )

    agent_session_id = session.start()
    print(f"Agent started: {agent_session_id}")

    session.stop()


if __name__ == "__main__":
    main()
```

## Presets vs BYOK

- Presets: fastest path, no vendor keys in app code
- BYOK: most control, your keys and your vendor configuration
