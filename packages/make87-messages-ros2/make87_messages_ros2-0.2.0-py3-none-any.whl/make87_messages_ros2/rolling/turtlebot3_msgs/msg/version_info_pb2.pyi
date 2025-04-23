from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VersionInfo(_message.Message):
    __slots__ = ["hardware", "firmware", "software"]
    HARDWARE_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_FIELD_NUMBER: _ClassVar[int]
    hardware: str
    firmware: str
    software: str
    def __init__(self, hardware: _Optional[str] = ..., firmware: _Optional[str] = ..., software: _Optional[str] = ...) -> None: ...
