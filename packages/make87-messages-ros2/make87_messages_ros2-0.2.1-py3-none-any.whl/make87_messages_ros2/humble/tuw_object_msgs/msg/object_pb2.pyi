from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_pb2 as _twist_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object(_message.Message):
    __slots__ = ["header", "ids", "shape", "shape_variables", "ids_confidence", "pose", "twist"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    IDS_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ids: _containers.RepeatedScalarFieldContainer[int]
    shape: int
    shape_variables: _containers.RepeatedScalarFieldContainer[float]
    ids_confidence: _containers.RepeatedScalarFieldContainer[float]
    pose: _pose_pb2.Pose
    twist: _twist_pb2.Twist
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ids: _Optional[_Iterable[int]] = ..., shape: _Optional[int] = ..., shape_variables: _Optional[_Iterable[float]] = ..., ids_confidence: _Optional[_Iterable[float]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., twist: _Optional[_Union[_twist_pb2.Twist, _Mapping]] = ...) -> None: ...
