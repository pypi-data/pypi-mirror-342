from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrStatus8(_message.Message):
    __slots__ = ["header", "ros2_header", "canmsg", "history_fault_0", "history_fault_1", "history_fault_2", "history_fault_3", "history_fault_4", "history_fault_5", "history_fault_6", "history_fault_7"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FAULT_0_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FAULT_1_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FAULT_2_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FAULT_3_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FAULT_4_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FAULT_5_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FAULT_6_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FAULT_7_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    canmsg: str
    history_fault_0: int
    history_fault_1: int
    history_fault_2: int
    history_fault_3: int
    history_fault_4: int
    history_fault_5: int
    history_fault_6: int
    history_fault_7: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., history_fault_0: _Optional[int] = ..., history_fault_1: _Optional[int] = ..., history_fault_2: _Optional[int] = ..., history_fault_3: _Optional[int] = ..., history_fault_4: _Optional[int] = ..., history_fault_5: _Optional[int] = ..., history_fault_6: _Optional[int] = ..., history_fault_7: _Optional[int] = ...) -> None: ...
