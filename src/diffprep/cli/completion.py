from collections.abc import Callable
from enum import StrEnum
from typing import Annotated, get_args, get_origin

from pydantic_settings import BaseSettings


def enum_values_for_field(
    settings_cls: type[BaseSettings],
    field_name: str,
) -> list[str]:
    annotation = settings_cls.model_fields[field_name].annotation

    if get_origin(annotation) is Annotated:
        annotation = get_args(annotation)[0]

    if isinstance(annotation, type) and issubclass(annotation, StrEnum):
        return [member.value for member in annotation]

    return []


def description_for_field(
    settings_cls: type[BaseSettings],
    field_name: str,
) -> str:
    field = settings_cls.model_fields[field_name]
    return field.description or field_name.replace("_", " ").capitalize()


def enum_field_completion(
    settings_cls: type[BaseSettings],
    field_name: str,
) -> Callable[[str], list[str]]:
    values = enum_values_for_field(settings_cls, field_name)

    def complete(incomplete: str) -> list[str]:
        needle = incomplete.lower()
        return [value for value in values if value.lower().startswith(needle)]

    return complete
