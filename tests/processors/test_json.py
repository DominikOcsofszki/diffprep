import pytest

from diffprep.core import Settings
from diffprep.processors import get_processor
from diffprep.types import InputType

CASES_NORMAL = [
    {"data": '{"b":2,"a":1}', "expected": '{"a":1,"b":2}'},
    {"data": '{"c":3,"a":1,"b":2}', "expected": '{"a":1,"b":2,"c":3}'},
    {"data": '{"z":{"b":2,"a":1},"a":0}', "expected": '{"a":0,"z":{"a":1,"b":2}}'},
    {"data": '{"version":2,"a":1}', "expected": '{"a":1}'},
    {"data": '{"version":2,"a":1}', "expected": '{"a":1}'},
    {
        "data": '{"a":1,"meta":{"version":2,"x":3}}',
        "expected": '{"a":1,"meta":{"x":3}}',
    },
    {
        "data": '{"a":1,"meta":{"info":{"version":2,"b":4}}}',
        "expected": '{"a":1,"meta":{"info":{"b":4}}}',
    },
    {
        "data": '{"items":[{"version":1,"a":2},{"version":2,"b":3}]}',
        "expected": '{"items":[{"a":2},{"b":3}]}',
    },
    {
        "data": '{"data":{"items":[{"version":1,"a":2},{"b":3,"version":4}]}}',
        "expected": '{"data":{"items":[{"a":2},{"b":3}]}}',
    },
]


@pytest.mark.parametrize("case", CASES_NORMAL)
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
