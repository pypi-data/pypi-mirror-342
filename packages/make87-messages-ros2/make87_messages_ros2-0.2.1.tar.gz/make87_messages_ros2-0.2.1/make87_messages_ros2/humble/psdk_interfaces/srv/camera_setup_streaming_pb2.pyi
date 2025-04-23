from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraSetupStreamingRequest(_message.Message):
    __slots__ = ["header", "payload_index", "camera_source", "start_stop", "decoded_output"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_INDEX_FIELD_NUMBER: _ClassVar[int]
    CAMERA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    START_STOP_FIELD_NUMBER: _ClassVar[int]
    DECODED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    payload_index: int
    camera_source: int
    start_stop: bool
    decoded_output: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., payload_index: _Optional[int] = ..., camera_source: _Optional[int] = ..., start_stop: bool = ..., decoded_output: bool = ...) -> None: ...

class CameraSetupStreamingResponse(_message.Message):
    __slots__ = ["header", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
