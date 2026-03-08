import json

from diffprep.processors import register_processor
from diffprep.types import InputType, JSONValue


def _decode_json(data: bytes) -> JSONValue:
    try:
        return json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid JSON input") from exc


def _normalize_json(cleaned: JSONValue) -> bytes:
    normalized = json.dumps(
        cleaned,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return (normalized).encode("utf-8")


def _scrub_json(value: JSONValue) -> JSONValue:
    return value


@register_processor(InputType.JSON)
def prepare_json(data: bytes) -> bytes:
    parsed = _decode_json(data)
    cleaned = _scrub_json(parsed)
    return _normalize_json(cleaned)
