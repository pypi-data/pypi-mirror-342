from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import geo_path_pb2 as _geo_path_pb2
from make87_messages_ros2.humble.nav_msgs.msg import path_pb2 as _path_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PathToGeopathRequest(_message.Message):
    __slots__ = ["header", "path"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    path: _path_pb2.Path
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., path: _Optional[_Union[_path_pb2.Path, _Mapping]] = ...) -> None: ...

class PathToGeopathResponse(_message.Message):
    __slots__ = ["header", "success", "geo_path"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    GEO_PATH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    geo_path: _geo_path_pb2.GeoPath
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., geo_path: _Optional[_Union[_geo_path_pb2.GeoPath, _Mapping]] = ...) -> None: ...
