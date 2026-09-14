---
type: External Service Contract
title: Warranty Check — Contract
description: Contract for the warranty lookup service (model_name + serial_number + user_id → coverage).
tags: [external-services, warranty, contract]
status: draft
generated: {by: s2agent/scaffold, at: 2026-09-14T00:00:00Z}
service: warranty-check
version: "0.1.0"
auth: internal-service-token (server-side; never expose to LLM)
stale_after: 2026-10-14T00:00:00Z
sources:
  - id: oem-warranty
    resource: "OEM warranty statement per model (see products/<category>/<brand>/<model>/specs.md)"
    title: OEM warranty terms
---

# Warranty Check — Contract

Check warranty coverage for a specific unit. `model_name` must match a model
in `knowledge/products` (e.g. `LG DUALCOOL AI AS-Q20JWZE`); `serial_number`
identifies the unit; `user_id` (from `MyAppState.user_id`) scopes the lookup.

## Required Input Fields

```json
[
  {
    "field": "model_name",
    "type": "str",
    "source": "user message / product context",
    "description": "Exact model name, e.g. LG DUALCOOL AI AS-Q20JWZE. Normalize case/whitespace before lookup."
  },
  {
    "field": "serial_number",
    "type": "str",
    "source": "user message (nameplate / invoice)",
    "description": "Unit serial, e.g. SN-LG-8X4K2Q9Z. Never invent."
  },
  {
    "field": "user_id",
    "type": "str",
    "source": "MyAppState.user_id (injected, never asked from LLM)",
    "description": "Requesting account. Must be non-empty."
  }
]
```

## Optional Input Fields

```json
[
  {
    "field": "purchase_date",
    "type": "str",
    "default": null,
    "description": "YYYY-MM-DD from invoice; improves accuracy when serial registry lags."
  },
  {
    "field": "invoice_id",
    "type": "str",
    "default": null,
    "description": "Invoice/order reference, e.g. INV-2025-0881 or ORD-2026-004281."
  },
  {
    "field": "order_id",
    "type": "str",
    "default": null,
    "description": "Alias of invoice_id for order-backed purchases."
  },
  {
    "field": "app_session_id",
    "type": "str",
    "default": "MyAppState.app_session_id",
    "description": "Tracing / idempotency key."
  }
]
```

> If `model_name` is missing, ask which appliance + model (offer brand list from `knowledge/products`).
> If `serial_number` is missing, ask once and explain where to find it (nameplate / invoice).
> If `user_id` is missing from state, escalate — do not invent one.

## Outputs

```json
{
  "model_name": "LG DUALCOOL AI AS-Q20JWZE",
  "serial_number": "SN-LG-8X4K2Q9Z",
  "user_id": "nav",
  "warranty_status": "in_warranty",
  "coverage_type": "comprehensive + 5y compressor",
  "coverage_end_date": "2027-03-01",
  "eligible_for_claim": true
}
```

`warranty_status` enum: `in_warranty | expired | extended | unknown`.

## Errors

```json
[
  {
    "code": "MODEL_UNKNOWN",
    "when": "model_name not in catalog",
    "agent_behaviour": "Offer closest models from knowledge/products, ask to confirm."
  },
  {
    "code": "SERIAL_INVALID",
    "when": "bad format / checksum",
    "agent_behaviour": "Re-ask for serial with where-to-find hint."
  },
  {
    "code": "PROOF_REQUIRED",
    "when": "needs invoice",
    "agent_behaviour": "Ask for purchase_date + invoice_id/order_id."
  },
  {
    "code": "NOT_OWNER",
    "when": "unit registered to another account",
    "agent_behaviour": "Do not leak details; ask for proof of purchase + escalate."
  }
]
```

## Example Tool Call

```python
check_warranty(model_name="LG DUALCOOL AI AS-Q20JWZE", serial_number="SN-LG-8X4K2Q9Z", user_id="nav")
```

## Related

* [External Services Overview](../index.md)
* [Tools Doc](../tools-doc/index.md)
* Model specs: `knowledge/products/<category>/<brand>/<model>/specs.md`.
