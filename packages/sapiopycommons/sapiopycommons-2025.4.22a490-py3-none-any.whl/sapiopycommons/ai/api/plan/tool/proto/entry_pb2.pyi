from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BINARY: _ClassVar[DataType]
    JSON: _ClassVar[DataType]
    CSV: _ClassVar[DataType]
    TEXT: _ClassVar[DataType]
    IMAGE: _ClassVar[DataType]
BINARY: DataType
JSON: DataType
CSV: DataType
TEXT: DataType
IMAGE: DataType

class StepCsvHeaderRow(_message.Message):
    __slots__ = ("cells",)
    CELLS_FIELD_NUMBER: _ClassVar[int]
    cells: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cells: _Optional[_Iterable[str]] = ...) -> None: ...

class StepCsvRow(_message.Message):
    __slots__ = ("cells",)
    CELLS_FIELD_NUMBER: _ClassVar[int]
    cells: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cells: _Optional[_Iterable[str]] = ...) -> None: ...

class StepCsvData(_message.Message):
    __slots__ = ("header", "entries")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    header: StepCsvHeaderRow
    entries: _containers.RepeatedCompositeFieldContainer[StepCsvRow]
    def __init__(self, header: _Optional[_Union[StepCsvHeaderRow, _Mapping]] = ..., entries: _Optional[_Iterable[_Union[StepCsvRow, _Mapping]]] = ...) -> None: ...

class StepJsonData(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entries: _Optional[_Iterable[str]] = ...) -> None: ...

class StepTextData(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entries: _Optional[_Iterable[str]] = ...) -> None: ...

class StepBinaryData(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, entries: _Optional[_Iterable[bytes]] = ...) -> None: ...

class StepImageData(_message.Message):
    __slots__ = ("image_format", "entries")
    IMAGE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    image_format: str
    entries: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, image_format: _Optional[str] = ..., entries: _Optional[_Iterable[bytes]] = ...) -> None: ...

class StepEntryData(_message.Message):
    __slots__ = ("dataType", "binary_data", "csv_data", "json_data", "text_data", "image_data")
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    BINARY_DATA_FIELD_NUMBER: _ClassVar[int]
    CSV_DATA_FIELD_NUMBER: _ClassVar[int]
    JSON_DATA_FIELD_NUMBER: _ClassVar[int]
    TEXT_DATA_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    dataType: DataType
    binary_data: StepBinaryData
    csv_data: StepCsvData
    json_data: StepJsonData
    text_data: StepTextData
    image_data: StepImageData
    def __init__(self, dataType: _Optional[_Union[DataType, str]] = ..., binary_data: _Optional[_Union[StepBinaryData, _Mapping]] = ..., csv_data: _Optional[_Union[StepCsvData, _Mapping]] = ..., json_data: _Optional[_Union[StepJsonData, _Mapping]] = ..., text_data: _Optional[_Union[StepTextData, _Mapping]] = ..., image_data: _Optional[_Union[StepImageData, _Mapping]] = ...) -> None: ...

class StepEntryInputData(_message.Message):
    __slots__ = ("is_partial", "entry_data")
    IS_PARTIAL_FIELD_NUMBER: _ClassVar[int]
    ENTRY_DATA_FIELD_NUMBER: _ClassVar[int]
    is_partial: bool
    entry_data: StepEntryData
    def __init__(self, is_partial: bool = ..., entry_data: _Optional[_Union[StepEntryData, _Mapping]] = ...) -> None: ...

class StepEntryOutputData(_message.Message):
    __slots__ = ("entry_data",)
    ENTRY_DATA_FIELD_NUMBER: _ClassVar[int]
    entry_data: StepEntryData
    def __init__(self, entry_data: _Optional[_Union[StepEntryData, _Mapping]] = ...) -> None: ...
