from make87_messages_ros2.jazzy.automotive_platform_msgs.msg import gear_pb2 as _gear_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GearCommand(_message.Message):
    __slots__ = ["header", "command"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    command: _gear_pb2.Gear
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., command: _Optional[_Union[_gear_pb2.Gear, _Mapping]] = ...) -> None: ...
