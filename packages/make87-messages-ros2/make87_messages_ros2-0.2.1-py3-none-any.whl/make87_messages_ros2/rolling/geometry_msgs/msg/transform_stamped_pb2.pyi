from make87_messages_ros2.rolling.geometry_msgs.msg import transform_pb2 as _transform_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransformStamped(_message.Message):
    __slots__ = ["header", "child_frame_id", "transform"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CHILD_FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    child_frame_id: str
    transform: _transform_pb2.Transform
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., child_frame_id: _Optional[str] = ..., transform: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ...) -> None: ...
