from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResetCmd(_message.Message):
    __slots__ = ["header", "confirm", "reset_type", "reset_user_rpt_id", "reset_user_cmd_id_1", "reset_user_cmd_id_2", "reset_user_cmd_id_3", "reset_user_cmd_id_4", "disable_user_rpt_id", "reenable_default_cmd_id"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    RESET_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESET_USER_RPT_ID_FIELD_NUMBER: _ClassVar[int]
    RESET_USER_CMD_ID_1_FIELD_NUMBER: _ClassVar[int]
    RESET_USER_CMD_ID_2_FIELD_NUMBER: _ClassVar[int]
    RESET_USER_CMD_ID_3_FIELD_NUMBER: _ClassVar[int]
    RESET_USER_CMD_ID_4_FIELD_NUMBER: _ClassVar[int]
    DISABLE_USER_RPT_ID_FIELD_NUMBER: _ClassVar[int]
    REENABLE_DEFAULT_CMD_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    confirm: bool
    reset_type: int
    reset_user_rpt_id: bool
    reset_user_cmd_id_1: bool
    reset_user_cmd_id_2: bool
    reset_user_cmd_id_3: bool
    reset_user_cmd_id_4: bool
    disable_user_rpt_id: bool
    reenable_default_cmd_id: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., confirm: bool = ..., reset_type: _Optional[int] = ..., reset_user_rpt_id: bool = ..., reset_user_cmd_id_1: bool = ..., reset_user_cmd_id_2: bool = ..., reset_user_cmd_id_3: bool = ..., reset_user_cmd_id_4: bool = ..., disable_user_rpt_id: bool = ..., reenable_default_cmd_id: bool = ...) -> None: ...
