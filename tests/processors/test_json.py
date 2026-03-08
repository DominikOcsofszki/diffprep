import pytest

from diffprep.core import Settings
from diffprep.processors import get_processor
from diffprep.types import InputType

CASES = [
    {"data": '{"b":2,"a":1}', "expected": '{"a":1,"b":2}'},
    {"data": '{"c":3,"a":1,"b":2}', "expected": '{"a":1,"b":2,"c":3}'},
    {"data": '{"z":{"b":2,"a":1},"a":0}', "expected": '{"a":0,"z":{"a":1,"b":2}}'},
]


@pytest.mark.parametrize("case", CASES)
def test_prepare_json(
    case: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
    test_settings: Settings,
) -> None:
    monkeypatch.setattr(
        "diffprep.processors.json.get_settings",
        lambda: test_settings,
    )

    json_processor = get_processor(InputType.JSON)

    expected = case["expected"]
    if test_settings.normalize.trailing_newline:
        expected += "\n"

    assert json_processor(case["data"].encode()) == expected.encode()
