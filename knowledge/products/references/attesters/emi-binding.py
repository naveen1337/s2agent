"""Deterministic attester for the EMI computation (no LLM).

Reads a receipt {"inputs": {...}, "result": n} from stdin as JSON and
exits 0 with PASS iff result matches an independent re-derivation of the
sanctioned computation within 0.01. Consumer-side check.
"""
import json
import sys


def expected_emi(principal, annual_rate_pct, months):
    r = annual_rate_pct / 12 / 100
    if r == 0:
        return principal / months
    factor = (1 + r) ** months
    return principal * r * factor / (factor - 1)


def attest(receipt: dict) -> bool:
    try:
        i = receipt["inputs"]
        expected = expected_emi(i["principal"], i["annual_rate_pct"], i["months"])
        return abs(expected - receipt["result"]) < 0.01
    except (KeyError, TypeError, ZeroDivisionError):
        return False


if __name__ == "__main__":
    ok = attest(json.load(sys.stdin))
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
