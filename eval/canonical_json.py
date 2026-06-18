"""``eval/canonical_json.py`` — canonical serialization for ``trace_hash`` (Task 00.4).

Sorted-key, no-incidental-whitespace, stable serialization so a ``trace_hash``
recomputed from a sidecar on any machine matches the one stored in the
match-summary (the §3.3 / AC-3 join). Shared by the runner (write side) and any
offline re-hash / replay check (read side).

Discipline: structures that get hashed (trace records) must carry **integers,
strings, bools, and null only** — no floats — so serialization is exact.
``decision_latency_ms`` is therefore stored as an int. Rates (floats) live only
in ``summary.csv`` and the ledger, which are never hashed.

This is intentionally independent of Loa's ``lib/jcs.sh`` JCS canonicalizer:
that belongs to the L1–L7 audit chain; TurnTrace artifacts are app-zone
evidence files, not audit-envelope records (SDD §1.4 note).

stdlib only (NFR-7).
"""

from __future__ import annotations

import hashlib
import json


def canonical_dumps(obj) -> str:
    """Deterministic JSON text: sorted keys, compact separators, ASCII-escaped."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_hex(data) -> str:
    """SHA-256 hex digest of a str (utf-8) or bytes."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def hash_canonical(obj) -> str:
    """SHA-256 over the canonical serialization of ``obj``."""
    return sha256_hex(canonical_dumps(obj))
