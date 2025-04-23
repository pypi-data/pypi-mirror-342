from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SBASService(_message.Message):
    __slots__ = ["header", "ranging", "corrections", "integrity", "test_mode", "bad"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RANGING_FIELD_NUMBER: _ClassVar[int]
    CORRECTIONS_FIELD_NUMBER: _ClassVar[int]
    INTEGRITY_FIELD_NUMBER: _ClassVar[int]
    TEST_MODE_FIELD_NUMBER: _ClassVar[int]
    BAD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ranging: bool
    corrections: bool
    integrity: bool
    test_mode: bool
    bad: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ranging: bool = ..., corrections: bool = ..., integrity: bool = ..., test_mode: bool = ..., bad: bool = ...) -> None: ...
