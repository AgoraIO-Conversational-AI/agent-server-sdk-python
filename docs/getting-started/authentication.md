---
sidebar_position: 2
title: Authentication
description: Configure the Agora client with app credentials or Basic Auth.
---

# Authentication

The Agora Python SDK supports two authentication modes. **App credentials** is the recommended approach for most applications — the SDK automatically generates a ConvoAI token (`Authorization: agora token=<token>`) for every request.

## App Credentials (Recommended)

Pass your Agora App ID and App Certificate. The SDK generates a fresh ConvoAI token (combined RTC + RTM) for every API call automatically.

### Sync

```python
from agora_agent import Agora, Area

client = Agora(
    area=Area.US,
    app_id='your-app-id',
    app_certificate='your-app-certificate',
)
```

### Async

```python
from agora_agent import AsyncAgora, Area

client = AsyncAgora(
    area=Area.US,
    app_id='your-app-id',
    app_certificate='your-app-certificate',
)
```

## Basic Auth

Use your Agora customer ID and customer secret. The SDK sends `Authorization: Basic base64(customer_id:customer_secret)` on every request.

### Sync

```python
from agora_agent import Agora, Area

client = Agora(
    area=Area.US,
    app_id='your-app-id',
    app_certificate='your-app-certificate',
    customer_id='your-customer-id',
    customer_secret='your-customer-secret',
)
```

### Async

```python
from agora_agent import AsyncAgora, Area

client = AsyncAgora(
    area=Area.US,
    app_id='your-app-id',
    app_certificate='your-app-certificate',
    customer_id='your-customer-id',
    customer_secret='your-customer-secret',
)
```

## Pre-built token

Pass a manually generated `agora token=...` string via `auth_token`. Use this for debugging or when you want to control the REST API token lifecycle yourself:

```python
from agora_agent import Agora, Area
from agora_agent.agentkit.token import generate_convo_ai_token

raw_token = generate_convo_ai_token(
    app_id='your-app-id',
    app_certificate='your-app-certificate',
    channel_name='your-channel',
    account='1',
)

client = Agora(
    area=Area.US,
    app_id='your-app-id',
    app_certificate='your-app-certificate',
    auth_token=raw_token,  # SDK sets Authorization: agora token=<raw_token>
)
```

## Auth Mode Comparison

| Mode | When to use | What you need |
|---|---|---|
| **App credentials** | Most applications. SDK manages ConvoAI tokens per request. | `app_id` + `app_certificate` |
| **Pre-built token** | Debugging, or when you manage the REST API token lifecycle. | `app_id` + `app_certificate` + `auth_token` |
| **Basic Auth** | When using customer-level credentials from the Agora Console. | `app_id` + `app_certificate` + `customer_id` + `customer_secret` |

## Advanced: Manual Token Generation

For advanced use cases you can generate tokens directly:

```python
from agora_agent.agentkit.token import generate_rtc_token, generate_convo_ai_token

# RTC-only token (for channel join)
rtc_token = generate_rtc_token(
    app_id='your-app-id',
    app_certificate='your-app-certificate',
    channel='your-channel',
    uid=1,
    expiry_seconds=86400,  # default; max allowed by Agora is 24 hours (86400 s)
)

# ConvoAI token (RTC + RTM combined, for REST API auth and channel join)
convo_token = generate_convo_ai_token(
    app_id='your-app-id',
    app_certificate='your-app-certificate',
    channel_name='your-channel',
    account='1001',
    token_expire=86400,  # default; max allowed by Agora is 24 hours (86400 s)
)
auth_header = f'agora token={convo_token}'
```

### `generate_rtc_token()` Reference

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `app_id` | `str` | Yes | — | Agora App ID |
| `app_certificate` | `str` | Yes | — | Agora App Certificate |
| `channel` | `str` | Yes | — | Channel name |
| `uid` | `int` | Yes | — | User ID (0 = any) |
| `role` | `int` | No | `ROLE_PUBLISHER` (1) | RTC role (`ROLE_PUBLISHER` or `ROLE_SUBSCRIBER`) |
| `expiry_seconds` | `int` | No | `86400` | Token expiry in seconds (max: 86400 = 24 h) |

### `generate_convo_ai_token()` Reference

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `app_id` | `str` | Yes | — | Agora App ID |
| `app_certificate` | `str` | Yes | — | Agora App Certificate |
| `channel_name` | `str` | Yes | — | Channel the agent will join |
| `account` | `str` | Yes | — | Agent UID as a string (e.g. `"1001"`) |
| `token_expire` | `int` | No | `86400` | Seconds until token expires (max: 86400 = 24 h) |
| `privilege_expire` | `int` | No | `0` | Seconds until privileges expire (0 = same as `token_expire`) |

## Token expiry

When the SDK auto-generates a token (app credentials mode, or session without a pre-built `token`), the default lifetime is **86400 seconds (24 hours)** — the Agora maximum. You can customise this via `expires_in` on `create_session()`:

```python
from agora_agent.agentkit import expires_in_hours, expires_in_minutes

session = agent.create_session(
    client,
    channel='room-123',
    agent_uid='1',
    remote_uids=['100'],
    expires_in=expires_in_hours(12),    # 12-hour token
    # expires_in=expires_in_minutes(30),  # 30-minute token
)
```

`expires_in_hours()` and `expires_in_minutes()` validate the value and raise `ValueError` if it is ≤ 0, or warn and cap at 86400 if it exceeds 24 hours. Valid range: **1–86400 seconds**.

## Areas

The `area` parameter determines which Agora region your requests are routed to:

| Area | Region |
|---|---|
| `Area.US` | United States (west + east) |
| `Area.EU` | Europe (west + central) |
| `Area.AP` | Asia-Pacific (southeast + northeast) |
| `Area.CN` | Chinese mainland (east + north) |

See [Regional Routing](../guides/regional-routing.md) for advanced domain selection.
