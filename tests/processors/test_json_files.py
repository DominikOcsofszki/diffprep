from pathlib import Path

import pytest

from diffprep.processors import get_processor
from diffprep.types import InputType

BASE = Path("tests/files/json")

CASES = [
    (p, p.with_name(p.name.replace(".in.json", ".out.json")))
    for p in BASE.glob("*.in.json")
]


@pytest.mark.xfail(reason="feature not implemented yet -- whitespace issues")
@pytest.mark.parametrize("inp,expected", CASES)
def test_prepare_json(inp: Path, expected: Path) -> None:
    assert expected.exists(), f"Missing expected file for {inp.name}: {expected}"

    processor = get_processor(InputType.JSON)
    assert processor(inp.read_bytes()) == expected.read_bytes()
