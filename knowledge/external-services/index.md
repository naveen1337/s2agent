---
type: External Services Index
title: External Services — Overview
description: Index of mocked external service contracts used by s2agent tools.
tags: [external-services, index, contracts]
status: draft
generated: {by: s2agent/scaffold, at: 2026-09-14T00:00:00Z}
okf_version: "0.2"
---

# External Services — Overview

Mocked backend services the agent calls via LangChain `@tool` wrappers.
Each service has its own folder with a contract (`index.md`) defining
required/optional fields, outputs, and errors.

- `user_id` always comes from `MyAppState.user_id` — never ask the LLM to invent it.
- `app_session_id` comes from `MyAppState.app_session_id` for tracing.

## Services

* [Get Order Status](get-order-status/index.md) - order tracking by `order_id` + `user_id`.
* [Technician Status](technician-status/index.md) - service-visit tracking by `service_ticket_id` + `user_id`.
* [Warranty Check](warranty-check/index.md) - warranty lookup by `model_name` + `serial_number` + `user_id`.
* [Tools Doc](tools-doc/index.md) - how the three services map to `@tool` functions.

## Related

* [Product Knowledge Bundle](../products/index.md)
* Agent state: `MyAppState` in `main.py` (`user_id`, `app_session_id`, `messages`).
