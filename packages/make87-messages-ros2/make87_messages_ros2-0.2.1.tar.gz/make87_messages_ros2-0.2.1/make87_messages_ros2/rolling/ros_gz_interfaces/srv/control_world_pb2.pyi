from make87_messages_ros2.rolling.ros_gz_interfaces.msg import world_control_pb2 as _world_control_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControlWorldRequest(_message.Message):
    __slots__ = ["world_control"]
    WORLD_CONTROL_FIELD_NUMBER: _ClassVar[int]
    world_control: _world_control_pb2.WorldControl
    def __init__(self, world_control: _Optional[_Union[_world_control_pb2.WorldControl, _Mapping]] = ...) -> None: ...

class ControlWorldResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
