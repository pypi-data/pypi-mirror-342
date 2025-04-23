from make87_messages_ros2.jazzy.nav_msgs.msg import path_pb2 as _path_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IsPathValidRequest(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: _path_pb2.Path
    def __init__(self, path: _Optional[_Union[_path_pb2.Path, _Mapping]] = ...) -> None: ...

class IsPathValidResponse(_message.Message):
    __slots__ = ["is_valid", "invalid_pose_indices"]
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    INVALID_POSE_INDICES_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    invalid_pose_indices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, is_valid: bool = ..., invalid_pose_indices: _Optional[_Iterable[int]] = ...) -> None: ...
