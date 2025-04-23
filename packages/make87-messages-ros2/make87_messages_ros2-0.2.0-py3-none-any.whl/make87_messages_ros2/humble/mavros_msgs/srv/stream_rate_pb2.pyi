from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StreamRateRequest(_message.Message):
    __slots__ = ["header", "stream_id", "message_rate", "on_off"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_RATE_FIELD_NUMBER: _ClassVar[int]
    ON_OFF_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stream_id: int
    message_rate: int
    on_off: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stream_id: _Optional[int] = ..., message_rate: _Optional[int] = ..., on_off: bool = ...) -> None: ...

class StreamRateResponse(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
