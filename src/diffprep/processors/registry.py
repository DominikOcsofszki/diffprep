from collections.abc import Callable

from diffprep.cli.enums import InputType
from diffprep.processors.json import prepare_json
from diffprep.processors.xml import prepare_xml

type Processor = Callable[[bytes], bytes]


FORMAT_PROCESSORS: dict[InputType, Processor] = {
    InputType.JSON: prepare_json,
    InputType.XML: prepare_xml,
}


def get_processor(input_type: InputType) -> Processor:
    try:
        return FORMAT_PROCESSORS[input_type]
    except KeyError as exc:
        raise ValueError(f"Unsupported input type: {input_type}") from exc
