from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Steer(_message.Message):
    __slots__ = ["header", "module_name", "curvature", "max_curvature_rate"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    CURVATURE_FIELD_NUMBER: _ClassVar[int]
    MAX_CURVATURE_RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    module_name: str
    curvature: float
    max_curvature_rate: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., module_name: _Optional[str] = ..., curvature: _Optional[float] = ..., max_curvature_rate: _Optional[float] = ...) -> None: ...
