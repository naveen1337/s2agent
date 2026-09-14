---
type: Attested Computation
title: EMI for a financed amount
description: Monthly instalment for principal, rate and tenure per the reducing-balance formula.
tags: [finance, emi, pricing]
status: draft
generated: {by: s2agent/scaffold, at: 2026-09-14T00:00:00Z}
runtime: python
parameters:
  - {name: principal, type: number, required: true}
  - {name: annual_rate_pct, type: number, required: true}
  - {name: months, type: integer, required: true}
executor:
  resource: references/skills/run-python.md
  receipt: [inputs, result]
attester:
  resource: references/attesters/emi-binding.py
---
# Computation

```python
def emi(principal, annual_rate_pct, months):
    r = annual_rate_pct / 12 / 100
    if r == 0:
        return principal / months
    factor = (1 + r) ** months
    return principal * r * factor / (factor - 1)
```

The agent supplies only `principal`, `annual_rate_pct`, `months`; it MUST NOT author or edit the computation. Reducing-balance EMI per standard amortisation.
