from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetOriginRequest(_message.Message):
    __slots__ = ["header", "origin"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    origin: _geo_point_pb2.GeoPoint
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., origin: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ...) -> None: ...

class SetOriginResponse(_message.Message):
    __slots__ = ["header", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
