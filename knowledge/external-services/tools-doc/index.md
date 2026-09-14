---
type: External Services Tooling Guide
title: Tools Doc — @tool Wrappers for External Services
description: How the three external services map to LangChain @tool functions bound in main.py.
tags: [external-services, tools, langchain, contract]
status: draft
generated: {by: s2agent/scaffold, at: 2026-09-14T00:00:00Z}
okf_version: "0.2"
---

# Tools Doc — `@tool` Wrappers for External Services

Authoritative mapping between the service contracts and the LangChain tools
bound to the LLM in `main.py`. Docstrings double as tool descriptions —
keep them in sync with the contract folders.

## Tool to Service Map

```json
[
  {
    "tool_function": "get_order_status(order_id, user_id, ...)",
    "service": "get-order-status",
    "required_fields": ["order_id: str", "user_id: str"],
    "optional_fields": ["include_items: bool = True", "app_session_id: str | None"]
  },
  {
    "tool_function": "get_technician_status(service_ticket_id, user_id, ...)",
    "service": "technician-status",
    "required_fields": ["service_ticket_id: str", "user_id: str"],
    "optional_fields": ["technician_id: str | None", "app_session_id: str | None"]
  },
  {
    "tool_function": "check_warranty(model_name, serial_number, user_id, ...)",
    "service": "warranty-check",
    "required_fields": ["model_name: str", "serial_number: str", "user_id: str"],
    "optional_fields": ["purchase_date: str | None", "invoice_id: str | None", "app_session_id: str | None"]
  }
]
```

## Canonical Signatures (copy into `main.py`)

```python
from langchain_core.tools import tool

@tool
def get_order_status(order_id: str, user_id: str, include_items: bool = True) -> str:
    """Get the current status of a sales order by order_id for the given user_id."""

@tool
def get_technician_status(service_ticket_id: str, user_id: str, technician_id: str | None = None) -> str:
    """Get the current technician visit status by service_ticket_id for the given user_id."""

@tool
def check_warranty(model_name: str, serial_number: str, user_id: str, purchase_date: str | None = None, invoice_id: str | None = None) -> str:
    """Check warranty coverage by model_name + serial_number for the given user_id."""
```

## Field-Injection Rules

- `user_id` / `app_session_id`: always inject from `MyAppState` — the LLM must
  never be asked to supply them and must never invent them.
- `model_name`: normalize (strip, collapse spaces); validate against
  `knowledge/products` before calling; on `MODEL_UNKNOWN` offer closest matches.
- `order_id` / `service_ticket_id` / `serial_number`: verbatim from user except
  trim + uppercase; on invalid format re-ask once with an example.
- Never expose full technician phone, internal tokens, or raw HTTP payloads.

## Error Handling

- Return errors as short codes from the contract (`ORDER_NOT_FOUND`,
  `TICKET_NOT_FOUND`, `MODEL_UNKNOWN`, `NOT_OWNER`, …) so the LLM can branch.
- On `NOT_OWNER`: reply "no record found for this account" + escalate; leak nothing.
- On missing required field: ask exactly one targeted follow-up, then retry.

## Related

* [External Services Overview](../index.md)
* [Get Order Status](../get-order-status/index.md)
* [Technician Status](../technician-status/index.md)
* [Warranty Check](../warranty-check/index.md)
