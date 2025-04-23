from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DockRequest(_message.Message):
    __slots__ = ["header", "frame_id", "poses", "stop_topic", "stop_message_field", "stop_compare_value", "dist_threshold"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    POSES_FIELD_NUMBER: _ClassVar[int]
    STOP_TOPIC_FIELD_NUMBER: _ClassVar[int]
    STOP_MESSAGE_FIELD_FIELD_NUMBER: _ClassVar[int]
    STOP_COMPARE_VALUE_FIELD_NUMBER: _ClassVar[int]
    DIST_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    frame_id: str
    poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    stop_topic: str
    stop_message_field: str
    stop_compare_value: bool
    dist_threshold: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., frame_id: _Optional[str] = ..., poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., stop_topic: _Optional[str] = ..., stop_message_field: _Optional[str] = ..., stop_compare_value: bool = ..., dist_threshold: _Optional[float] = ...) -> None: ...

class DockResponse(_message.Message):
    __slots__ = ["header", "success", "message"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
