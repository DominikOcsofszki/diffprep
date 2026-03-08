from enum import StrEnum
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class InputType(StrEnum):
    JSON = "json"
    XML = "xml"


class NormalizeSettings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="DIFFPREP_",
        extra="ignore",
    )

    input_type: InputType = Field(
        ...,
        description="Input format.",
    )
