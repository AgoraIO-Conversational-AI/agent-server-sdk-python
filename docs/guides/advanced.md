---
sidebar_position: 9
title: Advanced
description: Debug logging, raw response data, retries, timeouts, and custom httpx client.
---

# Advanced

## Debug Logging

Enable HTTP request/response logging by passing `debug=True` when creating the client. This logs each request (method, URL, headers, body preview) and response (status, headers) before and after it is sent. Authorization headers are redacted.

```python
from agora_agent import Agora, Area

client = Agora(
    area=Area.US,
    app_id="YOUR_APP_ID",
    app_certificate="YOUR_APP_CERTIFICATE",
    debug=True,
)
# All requests (including session.start()) will be logged
session = agent.create_session(client, ...)
session.start()  # Logs: HTTP request POST .../agents/start ...
```

The SDK uses the `agora_agent` logger. To control output without `debug=True`, configure it directly:

```python
import logging
logging.getLogger("agora_agent").setLevel(logging.DEBUG)
```

`debug=True` is ignored when you pass a custom `httpx_client`; use an httpx client with `event_hooks` for logging in that case.

## Access Raw Response Data

Use `.with_raw_response` to get a client that returns raw responses with `.headers` and `.data`:

```python
from agora_agent import Agora, Area

client = Agora(
    area=Area.US,
    app_id="YOUR_APP_ID",
    app_certificate="YOUR_APP_CERTIFICATE",
)
response = client.agents.with_raw_response.start(...)
print(response.headers)
print(response.data)
```

## Retries

The SDK retries automatically with exponential backoff when a request returns:

- **408** (Timeout)
- **429** (Too Many Requests)
- **5XX** (Internal Server Errors)

Default retry limit: 2. Override with `max_retries` in request options:

```python
client.agents.start(..., request_options={"max_retries": 1})
```

## Timeouts

Default timeout is 60 seconds. Set at the client or per request:

```python
client = Agora(
    area=Area.US,
    app_id="YOUR_APP_ID",
    app_certificate="YOUR_APP_CERTIFICATE",
    timeout=20.0,
)

# Per-request override
client.agents.start(..., request_options={"timeout_in_seconds": 30})
```

## Custom httpx Client

Pass a custom `httpx.Client` or `httpx.AsyncClient` for proxies, custom transports, or other options:

```python
import httpx
from agora_agent import Agora, Area

client = Agora(
    area=Area.US,
    app_id="YOUR_APP_ID",
    app_certificate="YOUR_APP_CERTIFICATE",
    httpx_client=httpx.Client(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

Use `httpx.AsyncClient()` when constructing an `AsyncAgora` client.
