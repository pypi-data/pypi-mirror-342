from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Altitude(_message.Message):
    __slots__ = ["header", "altitude", "sigma"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    SIGMA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    altitude: float
    sigma: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., altitude: _Optional[float] = ..., sigma: _Optional[float] = ...) -> None: ...
