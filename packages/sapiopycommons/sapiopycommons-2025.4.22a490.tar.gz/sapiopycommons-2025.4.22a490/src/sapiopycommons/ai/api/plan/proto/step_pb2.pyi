from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StepIoInfo(_message.Message):
    __slots__ = ("step_io_number", "content_type", "io_name")
    STEP_IO_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    IO_NAME_FIELD_NUMBER: _ClassVar[int]
    step_io_number: int
    content_type: str
    io_name: str
    def __init__(self, step_io_number: _Optional[int] = ..., content_type: _Optional[str] = ..., io_name: _Optional[str] = ...) -> None: ...

class StepIoDetails(_message.Message):
    __slots__ = ("step_io_info", "description", "example", "validation")
    STEP_IO_INFO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXAMPLE_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_FIELD_NUMBER: _ClassVar[int]
    step_io_info: StepIoInfo
    description: str
    example: str
    validation: str
    def __init__(self, step_io_info: _Optional[_Union[StepIoInfo, _Mapping]] = ..., description: _Optional[str] = ..., example: _Optional[str] = ..., validation: _Optional[str] = ...) -> None: ...

class StepInputDetails(_message.Message):
    __slots__ = ("step_io_details", "paging_supported", "max_entries")
    STEP_IO_DETAILS_FIELD_NUMBER: _ClassVar[int]
    PAGING_SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    MAX_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    step_io_details: StepIoDetails
    paging_supported: bool
    max_entries: int
    def __init__(self, step_io_details: _Optional[_Union[StepIoDetails, _Mapping]] = ..., paging_supported: bool = ..., max_entries: _Optional[int] = ...) -> None: ...

class StepOutputDetails(_message.Message):
    __slots__ = ("step_io_details",)
    STEP_IO_DETAILS_FIELD_NUMBER: _ClassVar[int]
    step_io_details: StepIoDetails
    def __init__(self, step_io_details: _Optional[_Union[StepIoDetails, _Mapping]] = ...) -> None: ...
