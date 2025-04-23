from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RFBand(_message.Message):
    __slots__ = ["frequency", "bandwidth", "info"]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    frequency: int
    bandwidth: int
    info: int
    def __init__(self, frequency: _Optional[int] = ..., bandwidth: _Optional[int] = ..., info: _Optional[int] = ...) -> None: ...
