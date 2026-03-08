import json
import logging

from diffprep.core import get_settings
from diffprep.core.configs import JsonSettings, NormalizeSettings
from diffprep.processors import register_processor
from diffprep.types import InputType, JSONValue


def _decode_json(data: bytes) -> JSONValue:
    try:
        return json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid JSON input") from exc


def _scrub_json(value: JSONValue, drop_keys: set[str]) -> JSONValue:
    logging.debug(drop_keys)
    if isinstance(value, dict):
        return {
            key: _scrub_json(child, drop_keys)
            for key, child in value.items()
            if key not in drop_keys
        }

    if isinstance(value, list):
        return [_scrub_json(item, drop_keys) for item in value]

    return value


def _normalize_json(
    cleaned: JSONValue,
    *,
    json_settings: JsonSettings,
    normalize_settings: NormalizeSettings,
) -> bytes:
    separators = (",", ":") if json_settings.style == "compact" else None

    normalized = json.dumps(
        cleaned,
        sort_keys=json_settings.sort_keys,
        separators=separators,
        ensure_ascii=json_settings.ensure_ascii,
        indent=json_settings.indent,
    )

    if normalize_settings.trailing_newline:
        normalized += "\n"

    return normalized.encode("utf-8")


@register_processor(InputType.JSON)
def prepare_json(data: bytes) -> bytes:
    settings = get_settings()
    logging.debug(settings)

    parsed = _decode_json(data)
    cleaned = _scrub_json(parsed, settings.json_settings.drop_keys)

    return _normalize_json(
        cleaned,
        json_settings=settings.json_settings,
        normalize_settings=settings.normalize,
    )
