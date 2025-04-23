from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.octomap_msgs.msg import octomap_pb2 as _octomap_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetOctomapRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetOctomapResponse(_message.Message):
    __slots__ = ["header", "map"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map: _octomap_pb2.Octomap
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map: _Optional[_Union[_octomap_pb2.Octomap, _Mapping]] = ...) -> None: ...
