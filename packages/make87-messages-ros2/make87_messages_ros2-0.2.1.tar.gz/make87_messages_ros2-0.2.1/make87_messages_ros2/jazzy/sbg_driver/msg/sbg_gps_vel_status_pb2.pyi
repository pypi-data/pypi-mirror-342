from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SbgGpsVelStatus(_message.Message):
    __slots__ = ["vel_status", "vel_type"]
    VEL_STATUS_FIELD_NUMBER: _ClassVar[int]
    VEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    vel_status: int
    vel_type: int
    def __init__(self, vel_status: _Optional[int] = ..., vel_type: _Optional[int] = ...) -> None: ...
