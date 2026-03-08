from typing import Annotated

import typer

from diffprep.cli.completion import description_for_field, enum_field_completion
from diffprep.cli.enums import InputType, NormalizeSettings
from diffprep.cli.io import read_stdin_bytes, write_stdout_bytes
from diffprep.processors import get_processor

app = typer.Typer(help="Command-line JSON and XML diff preprocessor.")


@app.command()
def normalize(
    input_type: Annotated[
        InputType,
        typer.Option(
            "--type",
            help=description_for_field(NormalizeSettings, "input_type"),
            autocompletion=enum_field_completion(NormalizeSettings, "input_type"),
        ),
    ],
) -> None:
    try:
        data = read_stdin_bytes()
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    processor = get_processor(input_type)
    out = processor(data)
    write_stdout_bytes(out)


if __name__ == "__main__":
    app()
