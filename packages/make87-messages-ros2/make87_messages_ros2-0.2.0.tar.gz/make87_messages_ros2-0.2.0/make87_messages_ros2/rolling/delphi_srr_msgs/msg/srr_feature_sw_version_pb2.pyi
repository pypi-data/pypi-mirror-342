from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SrrFeatureSwVersion(_message.Message):
    __slots__ = ["header", "lcma_sw_version", "cta_sw_version"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LCMA_SW_VERSION_FIELD_NUMBER: _ClassVar[int]
    CTA_SW_VERSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    lcma_sw_version: int
    cta_sw_version: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., lcma_sw_version: _Optional[int] = ..., cta_sw_version: _Optional[int] = ...) -> None: ...
