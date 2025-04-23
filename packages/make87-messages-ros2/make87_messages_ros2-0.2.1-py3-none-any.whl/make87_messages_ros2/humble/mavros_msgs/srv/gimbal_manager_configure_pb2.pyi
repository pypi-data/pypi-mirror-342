from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalManagerConfigureRequest(_message.Message):
    __slots__ = ["header", "sysid_primary", "compid_primary", "sysid_secondary", "compid_secondary", "gimbal_device_id"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SYSID_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    COMPID_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    SYSID_SECONDARY_FIELD_NUMBER: _ClassVar[int]
    COMPID_SECONDARY_FIELD_NUMBER: _ClassVar[int]
    GIMBAL_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sysid_primary: int
    compid_primary: int
    sysid_secondary: int
    compid_secondary: int
    gimbal_device_id: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sysid_primary: _Optional[int] = ..., compid_primary: _Optional[int] = ..., sysid_secondary: _Optional[int] = ..., compid_secondary: _Optional[int] = ..., gimbal_device_id: _Optional[int] = ...) -> None: ...

class GimbalManagerConfigureResponse(_message.Message):
    __slots__ = ["header", "success", "result"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    result: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., result: _Optional[int] = ...) -> None: ...
