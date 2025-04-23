from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MotorSetpoint(_message.Message):
    __slots__ = ["header", "duty_cycle"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DUTY_CYCLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    duty_cycle: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., duty_cycle: _Optional[float] = ...) -> None: ...
