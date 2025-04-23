from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrStatusSwVersion(_message.Message):
    __slots__ = ["header", "ros2_header", "can_pbl_field_revision", "can_pbl_promote_revision", "can_sw_field_revision", "can_sw_promote_revision", "can_sw_release_revision", "can_pbl_release_revision"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_PBL_FIELD_REVISION_FIELD_NUMBER: _ClassVar[int]
    CAN_PBL_PROMOTE_REVISION_FIELD_NUMBER: _ClassVar[int]
    CAN_SW_FIELD_REVISION_FIELD_NUMBER: _ClassVar[int]
    CAN_SW_PROMOTE_REVISION_FIELD_NUMBER: _ClassVar[int]
    CAN_SW_RELEASE_REVISION_FIELD_NUMBER: _ClassVar[int]
    CAN_PBL_RELEASE_REVISION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    can_pbl_field_revision: int
    can_pbl_promote_revision: int
    can_sw_field_revision: int
    can_sw_promote_revision: int
    can_sw_release_revision: int
    can_pbl_release_revision: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., can_pbl_field_revision: _Optional[int] = ..., can_pbl_promote_revision: _Optional[int] = ..., can_sw_field_revision: _Optional[int] = ..., can_sw_promote_revision: _Optional[int] = ..., can_sw_release_revision: _Optional[int] = ..., can_pbl_release_revision: _Optional[int] = ...) -> None: ...
