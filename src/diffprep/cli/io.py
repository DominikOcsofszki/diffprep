import sys


def read_stdin_bytes() -> bytes:
    data = sys.stdin.buffer.read()
    if not data:
        raise ValueError("No input received on stdin.")
    return data


def write_stdout_bytes(data: bytes) -> None:
    sys.stdout.buffer.write(data)
