---
sidebar_position: 7
title: Pagination
description: Iterate over paginated list endpoints.
---

# Pagination

Paginated requests return a `SyncPager` or `AsyncPager` that you can iterate over.

```python
from agora_agent import Agora, Area

client = Agora(
    area=Area.US,
    app_id="YOUR_APP_ID",
    app_certificate="YOUR_APP_CERTIFICATE",
)
response = client.agents.list(client.app_id)

for item in response:
    print(item)
```

## Page-by-page iteration

```python
for page in response.iter_pages():
    print(page.response)  # typed response for this page
    for item in page:
        print(item)
```

With `AsyncAgora`, use `async for` when iterating over an async pager.
