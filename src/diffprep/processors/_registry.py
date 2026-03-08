from collections.abc import Callable, Mapping
from types import MappingProxyType

from diffprep.cli.enums import InputType

type Processor = Callable[[bytes], bytes]


class ProcessorRegistryError(Exception):
    """Base error for processor registry problems."""


class DuplicateProcessorError(ProcessorRegistryError):
    """Raised when a processor is registered twice for the same input type."""


class UnknownProcessorError(ProcessorRegistryError):
    """Raised when no processor exists for the requested input type."""


_PROCESSORS: dict[InputType, Processor] = {}


def register_processor(input_type: InputType) -> Callable[[Processor], Processor]:
    def decorator(processor: Processor) -> Processor:
        if input_type in _PROCESSORS:
            raise DuplicateProcessorError(
                f"Processor already registered for {input_type.value!r}"
            )
        _PROCESSORS[input_type] = processor
        return processor

    return decorator


def get_processor(input_type: InputType, /) -> Processor:
    processor = _PROCESSORS.get(input_type)
    if processor is None:
        available = ", ".join(
            item.value for item in sorted(_PROCESSORS, key=lambda t: t.value)
        )
        raise UnknownProcessorError(
            f"Unsupported input type {input_type.value!r}. "
            f"Available: {available or '<none>'}"
        )
    return processor


def list_processors() -> tuple[InputType, ...]:
    return tuple(sorted(_PROCESSORS, key=lambda t: t.value))


def processor_mapping() -> Mapping[InputType, Processor]:
    return MappingProxyType(_PROCESSORS)


def validate_registered_processors() -> None:
    missing = set(InputType) - _PROCESSORS.keys()
    if missing:
        missing_names = ", ".join(
            item.value for item in sorted(missing, key=lambda t: t.value)
        )
        raise RuntimeError(f"Missing processor registrations: {missing_names}")
