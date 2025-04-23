from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.mavros_msgs.msg import param_value_pb2 as _param_value_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParamSetRequest(_message.Message):
    __slots__ = ["header", "param_id", "value"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARAM_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    param_id: str
    value: _param_value_pb2.ParamValue
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., param_id: _Optional[str] = ..., value: _Optional[_Union[_param_value_pb2.ParamValue, _Mapping]] = ...) -> None: ...

class ParamSetResponse(_message.Message):
    __slots__ = ["header", "success", "value"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    value: _param_value_pb2.ParamValue
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., value: _Optional[_Union[_param_value_pb2.ParamValue, _Mapping]] = ...) -> None: ...
