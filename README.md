# Agoraio Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2Ffern-demo%2Fagoraio-python-sdk)
[![pypi](https://img.shields.io/pypi/v/agoraio-sdk)](https://pypi.python.org/pypi/agoraio-sdk)

The Agoraio Python library provides convenient access to the Agoraio APIs from Python.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Reference](#reference)
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

## Table of Contents

- [Installation](#installation)
- [Reference](#reference)
- [Usage](#usage)
- [Async Client](#async-client)
- [Exception Handling](#exception-handling)
- [Advanced](#advanced)
  - [Access Raw Response Data](#access-raw-response-data)
  - [Retries](#retries)
  - [Timeouts](#timeouts)
  - [Custom Client](#custom-client)
- [Contributing](#contributing)

## Installation

```sh
pip install agoraio-sdk
```

## Reference

A full reference for this library is available [here](https://github.com/fern-demo/agoraio-python-sdk/blob/HEAD/./reference.md).

## Usage

Instantiate and use the client with the following:

```python
from agoraio import Agora
from agoraio.agent_management import (
    AgentManagementStartRequestProperties,
    AgentManagementStartRequestPropertiesAdvancedFeatures,
    AgentManagementStartRequestPropertiesAsr,
    AgentManagementStartRequestPropertiesLlm,
    AgentManagementStartRequestPropertiesTts,
)

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.agent_management.start(
    appid="appid",
    name="unique_name",
    properties=AgentManagementStartRequestProperties(
        channel="channel_name",
        token="token",
        agent_rtc_uid="1001",
        remote_rtc_uids=["1002"],
        idle_timeout=120,
        advanced_features=AgentManagementStartRequestPropertiesAdvancedFeatures(
            enable_aivad=True,
        ),
        asr=AgentManagementStartRequestPropertiesAsr(
            language="en-US",
        ),
        tts=AgentManagementStartRequestPropertiesTts(
            vendor="microsoft",
            params={
                "key": "<your_tts_api_key>",
                "region": "eastus",
                "voice_name": "en-US-AndrewMultilingualNeural",
            },
        ),
        llm=AgentManagementStartRequestPropertiesLlm(
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

The SDK also exports an `async` client so that you can make non-blocking calls to our API.

```python
import asyncio

from agoraio import AsyncAgora
from agoraio.agent_management import (
    AgentManagementStartRequestProperties,
    AgentManagementStartRequestPropertiesAdvancedFeatures,
    AgentManagementStartRequestPropertiesAsr,
    AgentManagementStartRequestPropertiesLlm,
    AgentManagementStartRequestPropertiesTts,
)

client = AsyncAgora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)


async def main() -> None:
    await client.agent_management.start(
        appid="appid",
        name="unique_name",
        properties=AgentManagementStartRequestProperties(
            channel="channel_name",
            token="token",
            agent_rtc_uid="1001",
            remote_rtc_uids=["1002"],
            idle_timeout=120,
            advanced_features=AgentManagementStartRequestPropertiesAdvancedFeatures(
                enable_aivad=True,
            ),
            asr=AgentManagementStartRequestPropertiesAsr(
                language="en-US",
            ),
            tts=AgentManagementStartRequestPropertiesTts(
                vendor="microsoft",
                params={
                    "key": "<your_tts_api_key>",
                    "region": "eastus",
                    "voice_name": "en-US-AndrewMultilingualNeural",
                },
            ),
            llm=AgentManagementStartRequestPropertiesLlm(
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
from agoraio.core.api_error import ApiError

try:
    client.agent_management.start(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Pagination

Paginated requests will return a `SyncPager` or `AsyncPager`, which can be used as generators for the underlying object.

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
response = client.agent_management.list(
    appid="appid",
    channel="channel",
    from_time=1.1,
    to_time=1.1,
    state="0",
    limit=1,
    cursor="cursor",
)
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page
```

## Advanced

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.with_raw_response` property.
The `.with_raw_response` property returns a "raw" client that can be used to access the `.headers` and `.data` attributes.

```python
from agoraio import Agora

client = Agora(
    ...,
)
response = client.agent_management.with_raw_response.start(...)
print(response.headers)  # access the response headers
print(response.data)  # access the underlying object
pager = client.agent_management.list(...)
print(pager.response.headers)  # access the response headers for the first page
for item in pager:
    print(item)  # access the underlying object(s)
for page in pager.iter_pages():
    print(page.response.headers)  # access the response headers for each page
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
client.agent_management.start(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python

from agoraio import Agora

client = Agora(
    ...,
    timeout=20.0,
)


# Override timeout for a specific method
client.agent_management.start(..., request_options={
    "timeout_in_seconds": 1
})
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.

```python
import httpx
from agoraio import Agora

client = Agora(
    ...,
    httpx_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
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
