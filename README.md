# Agoraio Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2FAgoraIO-Conversational-AI%2Fagent-server-sdk-python)
[![pypi](https://img.shields.io/pypi/v/agent-server-sdk-python)](https://pypi.python.org/pypi/agent-server-sdk-python)

The Agora Conversational AI SDK provides convenient access to the Agora Conversational AI APIs, 
enabling you to build voice-powered AI agents with support for both cascading flows (ASR -> LLM -> TTS) 
and multimodal flows (MLLM) for real-time audio processing.


## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Reference](#reference)
- [Mllm Flow Multimodal](#mllm-flow-multimodal)
- [Mllm Flow Multimodal](#mllm-flow-multimodal)
- [Usage](#usage)
- [Async Client](#async-client)
- [Exception Handling](#exception-handling)
- [Pagination](#pagination)
- [Advanced](#advanced)
  - [Access Raw Response Data](#access-raw-response-data)
  - [Retries](#retries)
  - [Timeouts](#timeouts)
  - [Custom Client](#custom-client)
- [Contributing](#contributing)

## Installation

```sh
pip install agent-server-sdk-python
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

API reference documentation is available [here](https://docs.agora.io/en/conversational-ai/overview).

## Reference

A full reference for this library is available [here](https://github.com/AgoraIO-Conversational-AI/agent-server-sdk-python/blob/HEAD/./reference.md).

## MLLM Flow (Multimodal)

For real-time audio processing using OpenAI's Realtime API or Google Gemini Live, use the MLLM (Multimodal Large Language Model) flow instead of the cascading ASR -> LLM -> TTS flow. See the [MLLM Overview](https://docs.agora.io/en/conversational-ai/models/mllm/overview) for more details.

```python
from agora_agent import Agora, Area
from agora_agent.agentkit import (
    AdvancedFeatures,
    TurnDetectionConfig,
    TurnDetectionTypeValues,
)
from agora_agent.agents import (
    StartAgentsRequestProperties,
    StartAgentsRequestPropertiesMllm,
    StartAgentsRequestPropertiesMllmVendor,
    StartAgentsRequestPropertiesTts,
    StartAgentsRequestPropertiesTtsVendor,
    StartAgentsRequestPropertiesLlm,
)

client = Agora(
    area=Area.US,
    app_id="YOUR_APP_ID",
    app_certificate="YOUR_APP_CERTIFICATE",
)

client.agents.start(
    client.app_id,
    name="mllm_agent",
    properties=StartAgentsRequestProperties(
        channel="channel_name",
        token="your_token",
        agent_rtc_uid="1001",
        remote_rtc_uids=["1002"],
        idle_timeout=120,
        advanced_features=AdvancedFeatures(enable_mllm=True),
        mllm=StartAgentsRequestPropertiesMllm(
            url="wss://api.openai.com/v1/realtime",
            api_key="<your_openai_api_key>",
            vendor=StartAgentsRequestPropertiesMllmVendor.OPENAI,
            params={
                "model": "gpt-4o-realtime-preview",
                "voice": "alloy",
            },
            input_modalities=["audio"],
            output_modalities=["text", "audio"],
            greeting_message="Hello! I'm ready to chat in real-time.",
        ),
        turn_detection=TurnDetectionConfig(
            type=TurnDetectionTypeValues.SERVER_VAD,  # deprecated; use config.end_of_speech instead
            threshold=0.5,
            silence_duration_ms=500,
        ),
        # TTS and LLM are still required but not used when MLLM is enabled
        tts=StartAgentsRequestPropertiesTts(
            vendor=StartAgentsRequestPropertiesTtsVendor.MICROSOFT,
            params={},
        ),
        llm=StartAgentsRequestPropertiesLlm(
            url="https://api.openai.com/v1/chat/completions",
        ),
    ),
)
```

## MLLM Flow (Multimodal)

For real-time audio processing using OpenAI's Realtime API or Google Gemini Live, use the MLLM (Multimodal Large Language Model) flow instead of the cascading ASR -> LLM -> TTS flow. See the [MLLM Overview](https://docs.agora.io/en/conversational-ai/models/mllm/overview) for more details.

```python
from agora-agent-server-sdk import Agora
from agora-agent-server-sdk.agents import (
    StartAgentsRequestProperties,
    StartAgentsRequestPropertiesAdvancedFeatures,
    StartAgentsRequestPropertiesMllm,
    StartAgentsRequestPropertiesMllmVendor,
    StartAgentsRequestPropertiesTts,
    StartAgentsRequestPropertiesTtsVendor,
    StartAgentsRequestPropertiesLlm,
    StartAgentsRequestPropertiesTurnDetection,
    StartAgentsRequestPropertiesTurnDetectionType,
)

client = Agora(
    customer_id="YOUR_CUSTOMER_ID",
    customer_secret="YOUR_CUSTOMER_SECRET",
)

client.agents.start(
    appid="your_app_id",
    name="mllm_agent",
    properties=StartAgentsRequestProperties(
        channel="channel_name",
        token="your_token",
        agent_rtc_uid="1001",
        remote_rtc_uids=["1002"],
        idle_timeout=120,
        advanced_features=StartAgentsRequestPropertiesAdvancedFeatures(
            enable_mllm=True,
        ),
        mllm=StartAgentsRequestPropertiesMllm(
            url="wss://api.openai.com/v1/realtime",
            api_key="<your_openai_api_key>",
            vendor=StartAgentsRequestPropertiesMllmVendor.OPENAI,
            params={
                "model": "gpt-4o-realtime-preview",
                "voice": "alloy",
            },
            input_modalities=["audio"],
            output_modalities=["text", "audio"],
            greeting_message="Hello! I'm ready to chat in real-time.",
        ),
        turn_detection=StartAgentsRequestPropertiesTurnDetection(
            type=StartAgentsRequestPropertiesTurnDetectionType.SERVER_VAD,
            threshold=0.5,
            silence_duration_ms=500,
        ),
        # TTS and LLM are still required but not used when MLLM is enabled
        tts=StartAgentsRequestPropertiesTts(
            vendor=StartAgentsRequestPropertiesTtsVendor.MICROSOFT,
            params={},
        ),
        llm=StartAgentsRequestPropertiesLlm(
            url="https://api.openai.com/v1/chat/completions",
        ),
    ),
)
```


## Usage

Instantiate and use the client with the following:

```python
from agora_agent import Agora, MicrosoftTtsParams, Tts_Microsoft
from agora_agent.agents import (
    StartAgentsRequestProperties,
    StartAgentsRequestPropertiesAsr,
    StartAgentsRequestPropertiesLlm,
)

client = Agora(
    authorization="YOUR_AUTHORIZATION",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.agents.start(
    appid="appid",
    name="unique_name",
    properties=StartAgentsRequestProperties(
        channel="channel_name",
        token="token",
        agent_rtc_uid="1001",
        remote_rtc_uids=["1002"],
        idle_timeout=120,
        asr=StartAgentsRequestPropertiesAsr(
            language="en-US",
        ),
        tts=Tts_Microsoft(
            params=MicrosoftTtsParams(
                key="key",
                region="region",
                voice_name="voice_name",
            ),
        ),
        llm=StartAgentsRequestPropertiesLlm(
            url="https://api.openai.com/v1/chat/completions",
            api_key="<your_llm_key>",
            system_messages=[
                {"role": "system", "content": "You are a helpful chatbot."}
            ],
            params={"model": "gpt-4o-mini"},
            max_history=32,
            greeting_message="Hello, how can I assist you today?",
            failure_message="Please hold on a second.",
        ),
    ),
)
```

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API. Note that if you are constructing an Async httpx client class to pass into this client, use `httpx.AsyncClient()` instead of `httpx.Client()` (e.g. for the `httpx_client` parameter of this client).

```python
import asyncio

from agora_agent import AsyncAgora, MicrosoftTtsParams, Tts_Microsoft
from agora_agent.agents import (
    StartAgentsRequestProperties,
    StartAgentsRequestPropertiesAsr,
    StartAgentsRequestPropertiesLlm,
)

client = AsyncAgora(
    authorization="YOUR_AUTHORIZATION",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)


async def main() -> None:
    await client.agents.start(
        appid="appid",
        name="unique_name",
        properties=StartAgentsRequestProperties(
            channel="channel_name",
            token="token",
            agent_rtc_uid="1001",
            remote_rtc_uids=["1002"],
            idle_timeout=120,
            asr=StartAgentsRequestPropertiesAsr(
                language="en-US",
            ),
            tts=Tts_Microsoft(
                params=MicrosoftTtsParams(
                    key="key",
                    region="region",
                    voice_name="voice_name",
                ),
            ),
            llm=StartAgentsRequestPropertiesLlm(
                url="https://api.openai.com/v1/chat/completions",
                api_key="<your_llm_key>",
                system_messages=[
                    {"role": "system", "content": "You are a helpful chatbot."}
                ],
                params={"model": "gpt-4o-mini"},
                max_history=32,
                greeting_message="Hello, how can I assist you today?",
                failure_message="Please hold on a second.",
            ),
        ),
    )


asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from agora_agent.core.api_error import ApiError

try:
    client.agents.start(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Pagination

Paginated requests will return a `SyncPager` or `AsyncPager`, which can be used as generators for the underlying object.

```python
from agora_agent import Agora

client = Agora(
    authorization="YOUR_AUTHORIZATION",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
response = client.agents.list(
    appid="appid",
)
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page
```

```python
# You can also iterate through pages and access the typed response per page
pager = client.agents.list(...)
for page in pager.iter_pages():
    print(page.response)  # access the typed response for each page
    for item in page:
        print(item)
```

## Advanced

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.with_raw_response` property.
The `.with_raw_response` property returns a "raw" client that can be used to access the `.headers` and `.data` attributes.

```python
from agora_agent import Agora

client = Agora(
    ...,
)
response = client.agents.with_raw_response.start(...)
print(response.headers)  # access the response headers
print(response.data)  # access the underlying object
pager = client.agents.list(...)
print(pager.response)  # access the typed response for the first page
for item in pager:
    print(item)  # access the underlying object(s)
for page in pager.iter_pages():
    print(page.response)  # access the typed response for each page
    for item in page:
        print(item)  # access the underlying object(s)
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retryable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retryable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.agents.start(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python

from agora_agent import Agora

client = Agora(
    ...,
    timeout=20.0,
)


# Override timeout for a specific method
client.agents.start(..., request_options={
    "timeout_in_seconds": 1
})
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.

```python
import httpx
from agora_agent import Agora

client = Agora(
    ...,
    httpx_client=httpx.Client(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
