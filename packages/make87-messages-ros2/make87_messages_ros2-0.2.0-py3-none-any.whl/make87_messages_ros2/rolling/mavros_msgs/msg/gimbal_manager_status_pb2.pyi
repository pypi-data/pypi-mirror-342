from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalManagerStatus(_message.Message):
    __slots__ = ["header", "flags", "gimbal_device_id", "sysid_primary", "compid_primary", "sysid_secondary", "compid_secondary"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    GIMBAL_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SYSID_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    COMPID_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    SYSID_SECONDARY_FIELD_NUMBER: _ClassVar[int]
    COMPID_SECONDARY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    flags: int
    gimbal_device_id: int
    sysid_primary: int
    compid_primary: int
    sysid_secondary: int
    compid_secondary: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., flags: _Optional[int] = ..., gimbal_device_id: _Optional[int] = ..., sysid_primary: _Optional[int] = ..., compid_primary: _Optional[int] = ..., sysid_secondary: _Optional[int] = ..., compid_secondary: _Optional[int] = ...) -> None: ...
