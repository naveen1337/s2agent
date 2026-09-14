---
type: External Service Contract
title: Technician Status — Contract
description: Contract for the service-visit tracking service (service_ticket_id + user_id → visit status).
tags: [external-services, technician, contract]
status: draft
generated: {by: s2agent/scaffold, at: 2026-09-14T00:00:00Z}
service: technician-status
version: "0.1.0"
auth: internal-service-token (server-side; never expose to LLM)
stale_after: 2026-10-14T00:00:00Z
sources:
  - id: fsm-api
    resource: "Field Service Management API spec (attach canonical URL or references/ path)"
    title: FSM API specification
---

# Technician Status — Contract

Lookup the current status of a service/repair visit. Ownership is enforced:
`user_id` (from `MyAppState.user_id`) must own `service_ticket_id`.

## Required Input Fields

```json
[
  {
    "field": "service_ticket_id",
    "type": "str",
    "source": "user message",
    "description": "Service ticket, e.g. SRV-2026-01193. Aliases: ticket_id, appointment_id."
  },
  {
    "field": "user_id",
    "type": "str",
    "source": "MyAppState.user_id (injected, never asked from LLM)",
    "description": "Owner of the ticket. Must be non-empty."
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
    "field": "technician_id",
    "type": "str",
    "default": null,
    "description": "Disambiguation when a ticket has multiple visits."
  },
  {
    "field": "date",
    "type": "str",
    "default": null,
    "description": "Filter by visit date (YYYY-MM-DD)."
  }
]
```

> If `service_ticket_id` is missing, ask exactly one follow-up: "Please share your service ticket ID (e.g. SRV-2026-01193)."
> Never reveal full technician phone numbers — only masked form from the output.

## Outputs

```json
{
  "service_ticket_id": "SRV-2026-01193",
  "user_id": "nav",
  "visit_status": "en_route",
  "technician_name": "Ravi Kumar",
  "technician_phone_masked": "+91-98XXXXXX10",
  "eta": "2026-09-14T15:30:00+05:30",
  "visit_slot": "2026-09-14 14:00-17:00",
  "model_name": "Samsung WA70BG4441BY"
}
```

`visit_status` enum: `assigned | en_route | on_site | completed | rescheduled | cancelled`.

## Errors

```json
[
  {
    "code": "INVALID_TICKET_ID",
    "when": "bad format",
    "agent_behaviour": "Re-ask for ticket ID with example format."
  },
  {
    "code": "TICKET_NOT_FOUND",
    "when": "unknown ID",
    "agent_behaviour": "Say not found, offer to retry or escalate."
  },
  {
    "code": "NOT_OWNER",
    "when": "user_id doesn't own ticket",
    "agent_behaviour": "Do not leak details; say no visit found for this account + escalate."
  }
]
```

## Example Tool Call

```python
get_technician_status(service_ticket_id="SRV-2026-01193", user_id="nav")
```

## Related

* [External Services Overview](../index.md)
* [Tools Doc](../tools-doc/index.md)
