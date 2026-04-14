from __future__ import annotations

import json


def parse_json_or_empty(payload: str | None) -> dict:
    if not payload:
        return {}
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return {}
