---
type: External Service Contract
title: Get Order Status — Contract
description: Contract for the order-tracking service (order_id + user_id → status).
tags: [external-services, orders, contract]
status: draft
generated: {by: s2agent/scaffold, at: 2026-09-14T00:00:00Z}
service: get-order-status
version: "0.1.0"
auth: internal-service-token (server-side; never expose to LLM)
stale_after: 2026-10-14T00:00:00Z
sources:
  - id: oms-api
    resource: "Order Management System API spec (attach canonical URL or references/ path)"
    title: OMS API specification
---

# Get Order Status — Contract

Lookup the current status of a sales order. Ownership is enforced:
`user_id` (from `MyAppState.user_id`) must own `order_id`.

## Required Input Fields

```json
[
  {
    "field": "order_id",
    "type": "str",
    "source": "user message",
    "description": "Order identifier, e.g. ORD-2026-004281. Trim whitespace, uppercase."
  },
  {
    "field": "user_id",
    "type": "str",
    "source": "MyAppState.user_id (injected, never asked from LLM)",
    "description": "Owner of the order. Must be non-empty."
  }
]
```

## Optional Input Fields

```json
[
  {
    "field": "app_session_id",
    "type": "str",
    "default": "MyAppState.app_session_id",
    "description": "Tracing / idempotency key."
  },
  {
    "field": "include_items",
    "type": "bool",
    "default": true,
    "description": "Return line items."
  },
  {
    "field": "phone_last4",
    "type": "str",
    "default": null,
    "description": "Extra verification for guest checkout (4 digits)."
  }
]
```

> If `order_id` is missing, ask exactly one follow-up: "Please share your order ID (e.g. ORD-2026-004281)."
> If `user_id` is missing from state, escalate — do not invent one.

## Outputs

```json
{
  "order_id": "ORD-2026-004281",
  "user_id": "nav",
  "status": "shipped",
  "status_detail": "Packed at Jaipur hub",
  "estimated_delivery": "2026-09-18",
  "items": [{"model_name": "LG DUALCOOL AI AS-Q20JWZE", "qty": 1}],
  "tracking_url": "https://example.com/track/ORD-2026-004281"
}
```

`status` enum: `placed | confirmed | shipped | out_for_delivery | delivered | cancelled | returned`.

## Errors

```json
[
  {
    "code": "INVALID_ORDER_ID",
    "when": "bad format",
    "agent_behaviour": "Re-ask for order ID with example format."
  },
  {
    "code": "ORDER_NOT_FOUND",
    "when": "unknown ID",
    "agent_behaviour": "Say not found, offer to retry or escalate."
  },
  {
    "code": "NOT_OWNER",
    "when": "user_id doesn't own order",
    "agent_behaviour": "Do not leak details; say no order found for this account + escalate."
  }
]
```

## Example Tool Call

```python
get_order_status(order_id="ORD-2026-004281", user_id="nav")
```

## Related

* [External Services Overview](../index.md)
* [Tools Doc](../tools-doc/index.md)
* Product specs live under `/products/<category>/<brand>/<model>/specs.md`.
