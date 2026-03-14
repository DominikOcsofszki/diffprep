from pydantic import BaseModel

from diffprep.types import InputType


class CliOptions(BaseModel):
    input_type: InputType
