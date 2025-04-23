from make87_messages_ros2.rolling.rosbag2_test_msgdefs.msg import basic_msg_pb2 as _basic_msg_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ComplexMsg(_message.Message):
    __slots__ = ["b"]
    B_FIELD_NUMBER: _ClassVar[int]
    b: _basic_msg_pb2.BasicMsg
    def __init__(self, b: _Optional[_Union[_basic_msg_pb2.BasicMsg, _Mapping]] = ...) -> None: ...
