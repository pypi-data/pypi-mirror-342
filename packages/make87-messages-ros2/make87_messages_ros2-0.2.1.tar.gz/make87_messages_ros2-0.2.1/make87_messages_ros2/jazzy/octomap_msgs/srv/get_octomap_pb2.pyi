from make87_messages_ros2.jazzy.octomap_msgs.msg import octomap_pb2 as _octomap_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetOctomapRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetOctomapResponse(_message.Message):
    __slots__ = ["map"]
    MAP_FIELD_NUMBER: _ClassVar[int]
    map: _octomap_pb2.Octomap
    def __init__(self, map: _Optional[_Union[_octomap_pb2.Octomap, _Mapping]] = ...) -> None: ...
