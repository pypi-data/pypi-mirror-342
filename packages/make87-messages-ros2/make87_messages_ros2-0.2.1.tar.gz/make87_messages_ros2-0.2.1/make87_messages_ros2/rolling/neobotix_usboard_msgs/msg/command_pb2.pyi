from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Command(_message.Message):
    __slots__ = ["header", "command", "command_data", "set_num", "paraset_byte6", "paraset_byte5", "paraset_byte4", "paraset_byte3", "paraset_byte2", "paraset_byte1", "set_active_9to16", "set_active_1to8"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    COMMAND_DATA_FIELD_NUMBER: _ClassVar[int]
    SET_NUM_FIELD_NUMBER: _ClassVar[int]
    PARASET_BYTE6_FIELD_NUMBER: _ClassVar[int]
    PARASET_BYTE5_FIELD_NUMBER: _ClassVar[int]
    PARASET_BYTE4_FIELD_NUMBER: _ClassVar[int]
    PARASET_BYTE3_FIELD_NUMBER: _ClassVar[int]
    PARASET_BYTE2_FIELD_NUMBER: _ClassVar[int]
    PARASET_BYTE1_FIELD_NUMBER: _ClassVar[int]
    SET_ACTIVE_9TO16_FIELD_NUMBER: _ClassVar[int]
    SET_ACTIVE_1TO8_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    command: int
    command_data: int
    set_num: int
    paraset_byte6: int
    paraset_byte5: int
    paraset_byte4: int
    paraset_byte3: int
    paraset_byte2: int
    paraset_byte1: int
    set_active_9to16: int
    set_active_1to8: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., command: _Optional[int] = ..., command_data: _Optional[int] = ..., set_num: _Optional[int] = ..., paraset_byte6: _Optional[int] = ..., paraset_byte5: _Optional[int] = ..., paraset_byte4: _Optional[int] = ..., paraset_byte3: _Optional[int] = ..., paraset_byte2: _Optional[int] = ..., paraset_byte1: _Optional[int] = ..., set_active_9to16: _Optional[int] = ..., set_active_1to8: _Optional[int] = ...) -> None: ...
