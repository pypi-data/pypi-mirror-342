from make87_messages_ros2.jazzy.geometry_msgs.msg import transform_pb2 as _transform_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Link(_message.Message):
    __slots__ = ["from_id", "to_id", "type", "transform", "information"]
    FROM_ID_FIELD_NUMBER: _ClassVar[int]
    TO_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    INFORMATION_FIELD_NUMBER: _ClassVar[int]
    from_id: int
    to_id: int
    type: int
    transform: _transform_pb2.Transform
    information: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, from_id: _Optional[int] = ..., to_id: _Optional[int] = ..., type: _Optional[int] = ..., transform: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ..., information: _Optional[_Iterable[float]] = ...) -> None: ...
