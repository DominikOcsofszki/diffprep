from pytest import MonkeyPatch
from typer.testing import CliRunner

from diffprep.cli.app import app
from diffprep.processors import Processor
from diffprep.types import InputType


def test_normalize_json_happy_path(
    runner: CliRunner,
    monkeypatch: MonkeyPatch,
) -> None:
    read_called = False
    wrote: bytes | None = None

    def fake_read_stdin_bytes() -> bytes:
        nonlocal read_called
        read_called = True
        return b'{"b":2,"a":1}'

    def fake_processor(data: bytes) -> bytes:
        assert data == b'{"b":2,"a":1}'
        return b'{"a":1,"b":2}'

    def fake_get_processor(input_type: InputType) -> Processor:
        assert input_type is InputType.JSON
        return fake_processor

    def fake_write_stdout_bytes(data: bytes) -> None:
        nonlocal wrote
        wrote = data

    monkeypatch.setattr("diffprep.cli.app.read_stdin_bytes", fake_read_stdin_bytes)
    monkeypatch.setattr("diffprep.cli.app.get_processor", fake_get_processor)
    monkeypatch.setattr("diffprep.cli.app.write_stdout_bytes", fake_write_stdout_bytes)

    result = runner.invoke(app, ["--type", "json"])

    assert result.exit_code == 0, result.output
    assert read_called
    assert wrote == b'{"a":1,"b":2}'
