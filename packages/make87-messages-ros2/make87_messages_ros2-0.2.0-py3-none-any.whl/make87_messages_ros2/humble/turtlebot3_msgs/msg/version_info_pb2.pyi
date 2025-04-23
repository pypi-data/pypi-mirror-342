from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VersionInfo(_message.Message):
    __slots__ = ["header", "hardware", "firmware", "software"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    hardware: str
    firmware: str
    software: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., hardware: _Optional[str] = ..., firmware: _Optional[str] = ..., software: _Optional[str] = ...) -> None: ...
