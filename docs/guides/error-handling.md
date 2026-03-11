---
sidebar_position: 6
title: Error Handling
description: Handle API errors with ApiError and subclasses.
---

# Error Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of `ApiError` is raised.

```python
from agora_agent.core.api_error import ApiError

try:
    client.agents.start(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

Use this for both the agentkit layer (e.g. `session.start()`) and direct client calls (`client.agents.start(...)`).
