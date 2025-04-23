from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonitoringCase(_message.Message):
    __slots__ = ["header", "monitoring_case_number", "fields", "fields_valid"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    FIELDS_VALID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    monitoring_case_number: int
    fields: _containers.RepeatedScalarFieldContainer[int]
    fields_valid: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., monitoring_case_number: _Optional[int] = ..., fields: _Optional[_Iterable[int]] = ..., fields_valid: _Optional[_Iterable[bool]] = ...) -> None: ...
