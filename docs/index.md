---
sidebar_position: 1
title: Overview
description: The Agora Conversational AI Python SDK — install, concepts, and examples.
---

# Agora Conversational AI Python SDK

The Agora Conversational AI Python SDK lets you build voice-powered AI agents that combine speech recognition, large language models, text-to-speech, and optional digital avatars — all routed through Agora's global real-time network.

## Sync and Async Clients

The Python SDK provides two client classes:

- **`Agora`** — synchronous client backed by `httpx.Client`. Use this in scripts, Flask apps, or anywhere synchronous code is natural.
- **`AsyncAgora`** — asynchronous client backed by `httpx.AsyncClient`. Use this in `asyncio` applications, FastAPI, or any async framework.

Both clients expose the same capabilities. Choose whichever fits your application's concurrency model.

## Two Conversation Flows

### Cascading Flow (ASR → LLM → TTS)

Speech-to-text transcribes audio, a text LLM generates a response, and text-to-speech renders it as audio. This is the most flexible flow — you can mix and match vendors for each stage.

### MLLM Flow (Multimodal LLM)

A multimodal model like OpenAI Realtime or Vertex AI Gemini Live handles audio input and output end-to-end, with no separate STT/TTS step.

## Two-Layer Architecture

```
+--------------------------------------------------+
|                Developer API                      |
|  Agent  ·  AgentSession  ·  Vendors  ·  Token     |  <- agentkit/ (hand-written)
+--------------------------------------------------+
|             Agora / AsyncAgora + Pool             |  <- pool_client.py (hand-written)
+--------------------------------------------------+
|          Fern-generated Client Core               |
|  AgentsClient · TelephonyClient · TypeSystem      |  <- generated, for advanced use
+--------------------------------------------------+
```

The **agentkit layer** (`agora_agent.agentkit`) is the primary developer-facing API. It provides the `Agent` builder, `AgentSession` lifecycle, typed vendor classes, and token helpers. You rarely need to use the Fern-generated layer directly, but it is accessible via `session.raw` when needed.

## Navigation

| Section | What you will learn |
|---|---|
| [Installation](./getting-started/installation.md) | Install the SDK and prerequisites |
| [Authentication](./getting-started/authentication.md) | Configure client credentials |
| [Quick Start](./getting-started/quick-start.md) | Build and run your first agent |
| [Architecture](./concepts/architecture.md) | Understand the SDK layers and client types |
| [Agent](./concepts/agent.md) | Configure agents with the fluent builder |
| [AgentSession](./concepts/session.md) | Manage the agent lifecycle |
| [Vendors](./concepts/vendors.md) | Browse all LLM, TTS, STT, MLLM, and Avatar providers |
| [Cascading Flow](./guides/cascading-flow.md) | Build an ASR → LLM → TTS pipeline |
| [MLLM Flow](./guides/mllm-flow.md) | Use OpenAI Realtime or Vertex AI for end-to-end audio |
| [Avatars](./guides/avatars.md) | Add a digital avatar with HeyGen or Akool |
| [Regional Routing](./guides/regional-routing.md) | Route requests to the nearest region |
| [Error Handling](./guides/error-handling.md) | Handle API errors with ApiError |
| [Pagination](./guides/pagination.md) | Iterate over paginated list endpoints |
| [Advanced](./guides/advanced.md) | Raw response, retries, timeouts, custom httpx client |
| [Low-Level API](./guides/low-level-api.md) | Direct client.agents.start() without the builder |
| [Client Reference](./reference/client.md) | Full Agora/AsyncAgora API |
| [Agent Reference](./reference/agent.md) | Full Agent builder API |
| [Session Reference](./reference/session.md) | Full AgentSession/AsyncAgentSession API |
| [Vendor Reference](./reference/vendors.md) | Constructor options for all vendor classes |
