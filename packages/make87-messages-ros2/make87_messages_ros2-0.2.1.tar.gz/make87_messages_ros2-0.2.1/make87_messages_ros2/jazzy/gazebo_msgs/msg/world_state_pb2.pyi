from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import twist_pb2 as _twist_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import wrench_pb2 as _wrench_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorldState(_message.Message):
    __slots__ = ["header", "name", "pose", "twist", "wrench"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    WRENCH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: _containers.RepeatedScalarFieldContainer[str]
    pose: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    twist: _containers.RepeatedCompositeFieldContainer[_twist_pb2.Twist]
    wrench: _containers.RepeatedCompositeFieldContainer[_wrench_pb2.Wrench]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[_Iterable[str]] = ..., pose: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., twist: _Optional[_Iterable[_Union[_twist_pb2.Twist, _Mapping]]] = ..., wrench: _Optional[_Iterable[_Union[_wrench_pb2.Wrench, _Mapping]]] = ...) -> None: ...
