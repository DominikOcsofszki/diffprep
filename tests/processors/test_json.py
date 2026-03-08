import pytest

from diffprep.processors import get_processor
from diffprep.types import InputType

CASES = [
    {"data": '{"b":2,"a":1}', "expected": '{"a":1,"b":2}'},
    {"data": '{"c":3,"a":1,"b":2}', "expected": '{"a":1,"b":2,"c":3}'},
    {"data": '{"z":{"b":2,"a":1},"a":0}', "expected": '{"a":0,"z":{"a":1,"b":2}}'},
]


@pytest.mark.parametrize("case", CASES)
def test_prepare_json(case: dict[str, str]) -> None:
    json_processor = get_processor(InputType.JSON)
    assert json_processor(case["data"].encode()) == case["expected"].encode()
