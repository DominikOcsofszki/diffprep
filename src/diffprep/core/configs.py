import logging
from functools import lru_cache
from typing import ClassVar, Literal, override

from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)

logger = logging.getLogger(__name__)


class NormalizeSettings(BaseModel):
    trailing_newline: bool = True


class JsonSettings(BaseModel):
    drop_keys: set[str] = Field(default_factory=set)
    indent: int | str | None = 4
    sort_keys: bool = True
    ensure_ascii: bool = False
    style: Literal["pretty", "compact"] = "pretty"


class XmlSettings(BaseModel):
    drop_tags: set[str] = Field(default_factory=set)
    drop_attrs: set[str] = Field(default_factory=set)
    indent: int = 4
    pretty: bool = True
    declaration: bool = False
    sort_attrs: bool = True
    strip_text: bool = True


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        extra="ignore",
        pyproject_toml_table_header=("tool", "diffprep"),
        pyproject_toml_depth=3,
    )

    normalize: NormalizeSettings = Field(default_factory=NormalizeSettings)
    json_settings: JsonSettings = Field(default_factory=JsonSettings)
    xml_settings: XmlSettings = Field(default_factory=XmlSettings)

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
        return (
            init_settings,
            PyprojectTomlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    logger.debug("Settings initialized: %s", settings)
    return settings
