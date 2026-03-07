import logging
from functools import lru_cache
from typing import ClassVar, override

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        extra="ignore",
        pyproject_toml_table_header=("tool", "diffprep"),
        pyproject_toml_depth=3,
    )

    json_drop_keys: set[str] = Field(default_factory=set)
    xml_drop_tags: set[str] = Field(default_factory=set)
    xml_drop_attrs: set[str] = Field(default_factory=set)

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
