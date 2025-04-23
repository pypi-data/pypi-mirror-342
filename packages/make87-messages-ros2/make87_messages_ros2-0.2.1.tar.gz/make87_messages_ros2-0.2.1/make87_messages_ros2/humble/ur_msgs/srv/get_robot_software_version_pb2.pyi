from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRobotSoftwareVersionRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetRobotSoftwareVersionResponse(_message.Message):
    __slots__ = ["header", "major", "minor", "bugfix", "build"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    BUGFIX_FIELD_NUMBER: _ClassVar[int]
    BUILD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    major: int
    minor: int
    bugfix: int
    build: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., major: _Optional[int] = ..., minor: _Optional[int] = ..., bugfix: _Optional[int] = ..., build: _Optional[int] = ...) -> None: ...
