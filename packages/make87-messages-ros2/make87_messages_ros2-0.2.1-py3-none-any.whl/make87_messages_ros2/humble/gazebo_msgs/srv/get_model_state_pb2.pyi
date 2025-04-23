from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_pb2 as _twist_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetModelStateRequest(_message.Message):
    __slots__ = ["header", "model_name", "relative_entity_name"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    model_name: str
    relative_entity_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., model_name: _Optional[str] = ..., relative_entity_name: _Optional[str] = ...) -> None: ...

class GetModelStateResponse(_message.Message):
    __slots__ = ["header", "ros2_header", "pose", "twist", "success", "status_message"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    pose: _pose_pb2.Pose
    twist: _twist_pb2.Twist
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., twist: _Optional[_Union[_twist_pb2.Twist, _Mapping]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
