from collections.abc import Callable
from enum import StrEnum
from typing import Annotated, get_args, get_origin

from pydantic import BaseModel


def enum_values_for_field(
    settings_cls: type[BaseModel],
    field_name: str,
) -> list[str]:
    annotation = settings_cls.model_fields[field_name].annotation
    origin = get_origin(annotation)
    if origin is Annotated:
        annotation = get_args(annotation)[0]
    if isinstance(annotation, type) and issubclass(annotation, StrEnum):
        return [member.value for member in annotation]
    return []


def description_for_field(
    settings_cls: type[BaseModel],
    field_name: str,
) -> str:
    field = settings_cls.model_fields[field_name]
    return field.description or ""


def enum_field_completion(
    settings_cls: type[BaseModel],
    field_name: str,
) -> Callable[[str], list[str]]:
    values = enum_values_for_field(settings_cls, field_name)
    return lambda incomplete: [
        value for value in values if value.startswith(incomplete)
    ]
