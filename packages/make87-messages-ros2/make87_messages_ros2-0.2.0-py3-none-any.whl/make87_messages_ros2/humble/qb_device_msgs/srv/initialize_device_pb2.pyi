from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.qb_device_msgs.msg import info_pb2 as _info_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InitializeDeviceRequest(_message.Message):
    __slots__ = ["header", "id", "activate", "rescan", "max_repeats"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_FIELD_NUMBER: _ClassVar[int]
    RESCAN_FIELD_NUMBER: _ClassVar[int]
    MAX_REPEATS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    activate: bool
    rescan: bool
    max_repeats: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., activate: bool = ..., rescan: bool = ..., max_repeats: _Optional[int] = ...) -> None: ...

class InitializeDeviceResponse(_message.Message):
    __slots__ = ["header", "success", "failures", "message", "info"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILURES_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    failures: int
    message: str
    info: _info_pb2.Info
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., failures: _Optional[int] = ..., message: _Optional[str] = ..., info: _Optional[_Union[_info_pb2.Info, _Mapping]] = ...) -> None: ...
