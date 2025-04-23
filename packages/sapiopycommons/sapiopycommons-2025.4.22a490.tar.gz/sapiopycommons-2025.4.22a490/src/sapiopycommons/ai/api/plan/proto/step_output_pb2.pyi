from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StepJsonOutputEntry(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: str
    def __init__(self, entry: _Optional[str] = ...) -> None: ...

class StepTextOutputEntry(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: str
    def __init__(self, entry: _Optional[str] = ...) -> None: ...

class StepCsvOutputEntry(_message.Message):
    __slots__ = ("cells",)
    CELLS_FIELD_NUMBER: _ClassVar[int]
    cells: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cells: _Optional[_Iterable[str]] = ...) -> None: ...

class StepBinaryOutputEntry(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: bytes
    def __init__(self, entry: _Optional[bytes] = ...) -> None: ...

class StepOutputEntry(_message.Message):
    __slots__ = ("json_output", "text_output", "csv_output", "binary_output")
    JSON_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TEXT_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    CSV_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    BINARY_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    json_output: StepJsonOutputEntry
    text_output: StepTextOutputEntry
    csv_output: StepCsvOutputEntry
    binary_output: StepBinaryOutputEntry
    def __init__(self, json_output: _Optional[_Union[StepJsonOutputEntry, _Mapping]] = ..., text_output: _Optional[_Union[StepTextOutputEntry, _Mapping]] = ..., csv_output: _Optional[_Union[StepCsvOutputEntry, _Mapping]] = ..., binary_output: _Optional[_Union[StepBinaryOutputEntry, _Mapping]] = ...) -> None: ...
