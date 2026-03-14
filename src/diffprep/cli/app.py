from __future__ import annotations

from typing import Annotated

import typer

from diffprep.cli.completion import description_for_field, enum_field_completion
from diffprep.cli.io import read_stdin_bytes, write_stdout_bytes
from diffprep.cli.models import CliOptions
from diffprep.cli.prompting import build_llm_prompt, build_prompt_context
from diffprep.core import get_settings
from diffprep.processors import get_processor
from diffprep.types import InputType

app = typer.Typer(help="Command-line JSON and XML diff preprocessor.")


@app.command()
def normalize(
    input_type: Annotated[
        InputType,
        typer.Option(
            "--type",
            help=description_for_field(CliOptions, "input_type"),
            autocompletion=enum_field_completion(CliOptions, "input_type"),
        ),
    ],
    question: Annotated[
        str | None,
        typer.Option(
            "--question",
            help=(
                "Generate an LLM-ready prompt instead of normalized output. "
                "The prompt includes the question, resolved settings, input, and output."
            ),
        ),
    ] = None,
) -> None:
    try:
        data = read_stdin_bytes()
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    processor = get_processor(input_type)
    out = processor(data)

    if question:
        context = build_prompt_context(
            question=question,
            input_type=input_type,
            original_input=data,
            normalized_output=out,
            settings=get_settings(),
        )
        prompt = build_llm_prompt(context)
        write_stdout_bytes(prompt.encode("utf-8"))
        return

    write_stdout_bytes(out)


if __name__ == "__main__":
    app()
