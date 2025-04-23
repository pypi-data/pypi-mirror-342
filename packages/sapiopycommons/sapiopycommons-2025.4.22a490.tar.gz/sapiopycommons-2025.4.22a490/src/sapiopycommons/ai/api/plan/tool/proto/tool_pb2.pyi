from sapiopycommons.ai.api.plan.tool.proto import entry_pb2 as _entry_pb2
from sapiopycommons.ai.api.plan.proto import step_pb2 as _step_pb2
from sapiopycommons.ai.api.session.proto import sapio_conn_info_pb2 as _sapio_conn_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepCsvHeaderRow as StepCsvHeaderRow
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepCsvRow as StepCsvRow
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepCsvData as StepCsvData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepJsonData as StepJsonData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepTextData as StepTextData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepBinaryData as StepBinaryData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepImageData as StepImageData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepEntryData as StepEntryData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepEntryInputData as StepEntryInputData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepEntryOutputData as StepEntryOutputData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import DataType as DataType
from sapiopycommons.ai.api.plan.proto.step_pb2 import StepIoInfo as StepIoInfo
from sapiopycommons.ai.api.plan.proto.step_pb2 import StepIoDetails as StepIoDetails
from sapiopycommons.ai.api.plan.proto.step_pb2 import StepInputDetails as StepInputDetails
from sapiopycommons.ai.api.plan.proto.step_pb2 import StepOutputDetails as StepOutputDetails
from sapiopycommons.ai.api.session.proto.sapio_conn_info_pb2 import SapioConnectionInfo as SapioConnectionInfo
from sapiopycommons.ai.api.session.proto.sapio_conn_info_pb2 import SapioUserSecretType as SapioUserSecretType

DESCRIPTOR: _descriptor.FileDescriptor
BINARY: _entry_pb2.DataType
JSON: _entry_pb2.DataType
CSV: _entry_pb2.DataType
TEXT: _entry_pb2.DataType
IMAGE: _entry_pb2.DataType
SESSION_TOKEN: _sapio_conn_info_pb2.SapioUserSecretType
PASSWORD: _sapio_conn_info_pb2.SapioUserSecretType

class ProcessStepRequest(_message.Message):
    __slots__ = ("sapio_user", "tool_name", "plan_instance_id", "step_instance_id", "invocation_id", "input_configs", "output_configs", "entry_data")
    SAPIO_USER_FIELD_NUMBER: _ClassVar[int]
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    PLAN_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    INVOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    ENTRY_DATA_FIELD_NUMBER: _ClassVar[int]
    sapio_user: _sapio_conn_info_pb2.SapioConnectionInfo
    tool_name: str
    plan_instance_id: int
    step_instance_id: int
    invocation_id: int
    input_configs: _containers.RepeatedCompositeFieldContainer[_step_pb2.StepIoInfo]
    output_configs: _containers.RepeatedCompositeFieldContainer[_step_pb2.StepIoInfo]
    entry_data: _containers.RepeatedCompositeFieldContainer[_entry_pb2.StepEntryInputData]
    def __init__(self, sapio_user: _Optional[_Union[_sapio_conn_info_pb2.SapioConnectionInfo, _Mapping]] = ..., tool_name: _Optional[str] = ..., plan_instance_id: _Optional[int] = ..., step_instance_id: _Optional[int] = ..., invocation_id: _Optional[int] = ..., input_configs: _Optional[_Iterable[_Union[_step_pb2.StepIoInfo, _Mapping]]] = ..., output_configs: _Optional[_Iterable[_Union[_step_pb2.StepIoInfo, _Mapping]]] = ..., entry_data: _Optional[_Iterable[_Union[_entry_pb2.StepEntryInputData, _Mapping]]] = ...) -> None: ...

class ProcessStepResponse(_message.Message):
    __slots__ = ("new_records", "log", "entry_data")
    NEW_RECORDS_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    ENTRY_DATA_FIELD_NUMBER: _ClassVar[int]
    new_records: _containers.RepeatedCompositeFieldContainer[StepRecord]
    log: _containers.RepeatedScalarFieldContainer[str]
    entry_data: _containers.RepeatedCompositeFieldContainer[_entry_pb2.StepEntryOutputData]
    def __init__(self, new_records: _Optional[_Iterable[_Union[StepRecord, _Mapping]]] = ..., log: _Optional[_Iterable[str]] = ..., entry_data: _Optional[_Iterable[_Union[_entry_pb2.StepEntryOutputData, _Mapping]]] = ...) -> None: ...

class ToolDetailsRequest(_message.Message):
    __slots__ = ("sapio_conn_info",)
    SAPIO_CONN_INFO_FIELD_NUMBER: _ClassVar[int]
    sapio_conn_info: _sapio_conn_info_pb2.SapioConnectionInfo
    def __init__(self, sapio_conn_info: _Optional[_Union[_sapio_conn_info_pb2.SapioConnectionInfo, _Mapping]] = ...) -> None: ...

class StepRecordFieldValue(_message.Message):
    __slots__ = ("string_value", "int_value", "double_value", "bool_value")
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    string_value: str
    int_value: int
    double_value: float
    bool_value: bool
    def __init__(self, string_value: _Optional[str] = ..., int_value: _Optional[int] = ..., double_value: _Optional[float] = ..., bool_value: bool = ...) -> None: ...

class StepRecord(_message.Message):
    __slots__ = ("fields",)
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: StepRecordFieldValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[StepRecordFieldValue, _Mapping]] = ...) -> None: ...
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.MessageMap[str, StepRecordFieldValue]
    def __init__(self, fields: _Optional[_Mapping[str, StepRecordFieldValue]] = ...) -> None: ...

class ToolDetails(_message.Message):
    __slots__ = ("name", "description", "input_configs", "output_configs")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INPUT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    input_configs: _containers.RepeatedCompositeFieldContainer[_step_pb2.StepIoDetails]
    output_configs: _containers.RepeatedCompositeFieldContainer[_step_pb2.StepIoDetails]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., input_configs: _Optional[_Iterable[_Union[_step_pb2.StepIoDetails, _Mapping]]] = ..., output_configs: _Optional[_Iterable[_Union[_step_pb2.StepIoDetails, _Mapping]]] = ...) -> None: ...

class ToolDetailsResponse(_message.Message):
    __slots__ = ("tool_framework_version", "tool_details")
    TOOL_FRAMEWORK_VERSION_FIELD_NUMBER: _ClassVar[int]
    TOOL_DETAILS_FIELD_NUMBER: _ClassVar[int]
    tool_framework_version: int
    tool_details: _containers.RepeatedCompositeFieldContainer[ToolDetails]
    def __init__(self, tool_framework_version: _Optional[int] = ..., tool_details: _Optional[_Iterable[_Union[ToolDetails, _Mapping]]] = ...) -> None: ...
