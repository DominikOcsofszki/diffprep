from __future__ import annotations

import logging
from typing import ClassVar, Literal, override

from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)

logger = logging.getLogger(__name__)


class LoggerSettings(BaseModel):
    level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = Field(
        default="INFO",
        description="Logging level.",
    )
    fmt: str = Field(
        default="%(filename)-16s:%(lineno)1d  %(message)s",
        description="Logging format string.",
    )
    disable_existing_loggers: bool = Field(
        default=False,
        description="Disable pre-existing loggers when configuring logging.",
    )


class NormalizeSettings(BaseModel):
    trailing_newline: bool = Field(
        default=True,
        description="Ensure normalized output ends with a trailing newline.",
    )


class JsonSettings(BaseModel):
    drop_keys: set[str] = Field(
        default_factory=set,
        description="JSON object keys to remove recursively before output.",
    )
    indent: int | str | None = Field(
        default=4,
        description="Indentation used for pretty JSON output.",
    )
    sort_keys: bool = Field(
        default=True,
        description="Sort JSON object keys for stable output.",
    )
    ensure_ascii: bool = Field(
        default=False,
        description="Escape non-ASCII characters in JSON output.",
    )
    style: Literal["pretty", "compact"] = Field(
        default="pretty",
        description="JSON output style.",
    )


class XmlSettings(BaseModel):
    drop_tags: set[str] = Field(
        default_factory=set,
        description="XML tags to remove recursively before output.",
    )
    drop_attrs: set[str] = Field(
        default_factory=set,
        description="XML attributes to remove from all elements.",
    )
    indent: int = Field(
        default=4,
        ge=0,
        description="Indentation used for pretty XML output.",
    )
    pretty: bool = Field(
        default=True,
        description="Pretty-print XML output.",
    )
    declaration: bool = Field(
        default=False,
        description="Include XML declaration in serialized output.",
    )
    sort_attrs: bool = Field(
        default=True,
        description="Sort XML attributes for stable output.",
    )
    strip_text: bool = Field(
        default=True,
        description="Strip surrounding whitespace from XML text nodes where applicable.",
    )


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        extra="ignore",
        pyproject_toml_table_header=("tool", "diffprep"),
        pyproject_toml_depth=3,
        env_prefix="DIFFPREP_",
        env_nested_delimiter="__",
    )

    normalize: NormalizeSettings = Field(default_factory=NormalizeSettings)
    json_settings: JsonSettings = Field(default_factory=JsonSettings)
    xml_settings: XmlSettings = Field(default_factory=XmlSettings)
    logger_settings: LoggerSettings = Field(default_factory=LoggerSettings)

    @classmethod
    @override
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        pyproject_settings = PyprojectTomlConfigSettingsSource(settings_cls)
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            pyproject_settings,
            file_secret_settings,
        )
