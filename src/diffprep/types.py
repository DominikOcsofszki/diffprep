from enum import StrEnum

type JSONValue = (
    dict[str, JSONValue] | list[JSONValue] | str | int | float | bool | None
)


class InputType(StrEnum):
    JSON = "json"
    XML = "xml"
