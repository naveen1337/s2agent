---
type: Reference
title: Run a python computation
description: Run instructions for python Attested Computations; returns a receipt with inputs and result.
tags: [reference, runtime, python]
status: draft
generated: {by: s2agent/scaffold, at: 2026-09-14T00:00:00Z}
---
# Steps

1. Load the computation fence from the concept body.
2. Bind only the declared `parameters` to caller-supplied values.
3. Execute and return the receipt as JSON: `{"inputs": {...}, "result": <number>}`.
