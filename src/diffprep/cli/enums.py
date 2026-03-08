from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from diffprep.types import InputType


class NormalizeSettings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="DIFFPREP_",
        extra="ignore",
    )

    input_type: InputType = Field(
        ...,
        description="Input format.",
    )
