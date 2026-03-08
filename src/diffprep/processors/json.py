import json

import canonicaljson

from diffprep.types import JSONValue


def decode_json(data: bytes) -> JSONValue:
    return json.loads(data)


def canonical_form(cleaned: JSONValue) -> bytes:
    return canonicaljson.encode_canonical_json(cleaned)


def prepare_json(data: bytes) -> bytes:
    parsed = decode_json(data)
    cleaned = scrub_json(parsed)
    return canonical_form(cleaned)


def scrub_json(value: JSONValue) -> JSONValue:
    return value
