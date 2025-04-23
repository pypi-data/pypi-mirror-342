from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.as2_msgs.msg import control_mode_pb2 as _control_mode_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetControlModeRequest(_message.Message):
    __slots__ = ["header", "control_mode"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONTROL_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    control_mode: _control_mode_pb2.ControlMode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., control_mode: _Optional[_Union[_control_mode_pb2.ControlMode, _Mapping]] = ...) -> None: ...

class SetControlModeResponse(_message.Message):
    __slots__ = ["header", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
