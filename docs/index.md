---
sidebar_position: 1
title: Overview
description: The Agora Conversational AI Python SDK — install, concepts, and examples.
---

# Agora Conversational AI Python SDK

The Agora Conversational AI Python SDK lets you build voice-powered AI agents on the [Agora Conversational AI](https://docs.agora.io/en/conversational-ai/overview) platform.

## Client models

- **`Agora`** for synchronous applications
- **`AsyncAgora`** for `asyncio` applications

## Conversation flows

**Cascading flow** uses ASR -> LLM -> TTS and supports the broadest set of vendor combinations.

**MLLM flow** uses a multimodal model such as OpenAI Realtime or Gemini Live for end-to-end audio.

## Choose a starting point

- Use [Quick Start](./getting-started/quick-start.md) if you want the recommended preset-based path with no vendor keys.
- Use [MLLM Flow](./guides/mllm-flow.md) if you want realtime end-to-end audio with OpenAI Realtime or Gemini Live.
- Use [Cascading Flow](./guides/cascading-flow.md) if you want separate ASR, LLM, and TTS vendors.

## SDK layers

| Layer | What it does | When to use |
|---|---|---|
| **Agentkit** (`Agent`, `AgentSession`, vendors, presets) | High-level builder pattern, lifecycle, typed vendors | Most use cases |
| **Fern-generated core** (`client.agents`, `client.telephony`) | Direct REST client mapping every API endpoint | Advanced use cases |

## Documentation

| Section | What you will learn |
|---|---|
| [Installation](./getting-started/installation.md) | Install the SDK and prerequisites |
| [Authentication](./getting-started/authentication.md) | Token auth for REST and RTC joins |
| [Quick Start](./getting-started/quick-start.md) | Recommended preset-based onboarding flow |
| [BYOK](./guides/byok.md) | Bring your own vendor credentials and config |
| [Architecture](./concepts/architecture.md) | Understand the SDK layers and client types |
| [Agent](./concepts/agent.md) | Configure agents with the fluent builder |
| [AgentSession](./concepts/session.md) | Manage the agent lifecycle |
| [Vendors](./concepts/vendors.md) | Browse all LLM, TTS, STT, MLLM, and Avatar providers |
| [Cascading Flow](./guides/cascading-flow.md) | Build an ASR -> LLM -> TTS pipeline |
| [MLLM Flow](./guides/mllm-flow.md) | Use OpenAI Realtime or Gemini Live for end-to-end audio |
| [Avatars](./guides/avatars.md) | Add a digital avatar with HeyGen or Akool |
| [Regional Routing](./guides/regional-routing.md) | Route requests to the nearest region |
| [Error Handling](./guides/error-handling.md) | Handle API errors with ApiError |
| [Pagination](./guides/pagination.md) | Iterate over paginated list endpoints |
| [Advanced](./guides/advanced.md) | Raw response, retries, timeouts, custom httpx client |
| [Low-Level API](./guides/low-level-api.md) | Direct `client.agents.start()` usage |
| [Client Reference](./reference/client.md) | Full `Agora` / `AsyncAgora` API |
| [Agent Reference](./reference/agent.md) | Full `Agent` builder API |
| [Session Reference](./reference/session.md) | Full `AgentSession` / `AsyncAgentSession` API |
| [Vendor Reference](./reference/vendors.md) | Constructor options for all vendor classes |
