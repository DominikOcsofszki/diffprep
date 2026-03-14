from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from diffprep.core.configs import Settings
from diffprep.types import InputType

DEFAULT_MAX_PROMPT_CHARS = 4_000


def render_settings_help(settings: BaseModel, prefix: str = "") -> str:
    lines: list[str] = []

    for name, field in settings.model_fields.items():
        value = getattr(settings, name)
        path = f"{prefix}.{name}" if prefix else name

        if isinstance(value, BaseModel):
            lines.append(render_settings_help(value, path))
        else:
            env = f"DIFFPREP_{path.replace('.', '__')}"
            desc = field.description or ""
            lines.append(f"{path} = {value!r}  ({env})  # {desc}")

    return "\n".join(lines)


class PromptContext(BaseModel):
    """Structured context passed to the LLM prompt renderer."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    question: str = Field(min_length=1)
    input_type: InputType
    original_input: str
    normalized_output: str
    settings: Settings

    @property
    def current_command(self) -> str:
        """CLI command that reproduces the current invocation."""
        return f"diffprep --type {self.input_type.value}"


def decode_bytes(data: bytes, /) -> str:
    """Decode bytes as UTF-8, replacing invalid sequences."""
    return data.decode("utf-8", errors="replace")


def truncate_text(text: str, /, *, max_chars: int = DEFAULT_MAX_PROMPT_CHARS) -> str:
    """Truncate text and append a notice if the text was shortened."""
    if len(text) <= max_chars:
        return text

    remaining = len(text) - max_chars
    return (
        f"{text[:max_chars]}\n\n"
        f"[truncated: showing first {max_chars} of {len(text)} characters; "
        f"{remaining} omitted]"
    )


def build_prompt_context(
    *,
    question: str,
    input_type: InputType,
    original_input: bytes,
    normalized_output: bytes,
    settings: Settings,
    max_chars: int = DEFAULT_MAX_PROMPT_CHARS,
) -> PromptContext:
    """Create the structured context used to generate the LLM prompt."""

    cleaned_question = question.strip()

    return PromptContext(
        question=cleaned_question,
        input_type=input_type,
        original_input=truncate_text(decode_bytes(original_input), max_chars=max_chars),
        normalized_output=truncate_text(
            decode_bytes(normalized_output),
            max_chars=max_chars,
        ),
        settings=settings,
    )


def build_llm_prompt(context: PromptContext) -> str:
    """Render the final LLM prompt string."""

    settings_text = context.settings.model_dump_json(indent=2, exclude_none=True)
    settings_help = render_settings_help(context.settings)

    return f"""--- PROMPT START ---

You are helping a user of the CLI tool `diffprep`.

Tool purpose:
`diffprep` preprocesses structured input such as JSON or XML so the output is more stable and useful for diffs.

User question:
{context.question}

Current command:
{context.current_command}

Settings (current values and env overrides):
{settings_help}

Input type:
{context.input_type.value}

Resolved settings:
{settings_text}

Original input:
{context.original_input}

Current output:
{context.normalized_output}

Please answer in a practical way.
Include:
1. what is likely missing or incorrect
2. the exact command, config, or environment variable change needed
3. a minimal working example
4. any common mistakes relevant to this case

--- PROMPT END ---
"""
