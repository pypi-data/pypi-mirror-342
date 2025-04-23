from make87_messages_ros2.rolling.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetPayloadRequest(_message.Message):
    __slots__ = ["mass", "center_of_gravity"]
    MASS_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_FIELD_NUMBER: _ClassVar[int]
    mass: float
    center_of_gravity: _vector3_pb2.Vector3
    def __init__(self, mass: _Optional[float] = ..., center_of_gravity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...

class SetPayloadResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
