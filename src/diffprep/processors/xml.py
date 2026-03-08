from diffprep.processors import register_processor
from diffprep.types import InputType


@register_processor(input_type=InputType.XML)
def prepare_xml(data: bytes) -> bytes:
    out: bytes = data
    return out
