from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.psdk_interfaces.msg import file_info_pb2 as _file_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraGetFileListInfoRequest(_message.Message):
    __slots__ = ["header", "payload_index"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    payload_index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., payload_index: _Optional[int] = ...) -> None: ...

class CameraGetFileListInfoResponse(_message.Message):
    __slots__ = ["header", "success", "file_list", "count"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FILE_LIST_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    file_list: _containers.RepeatedCompositeFieldContainer[_file_info_pb2.FileInfo]
    count: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., file_list: _Optional[_Iterable[_Union[_file_info_pb2.FileInfo, _Mapping]]] = ..., count: _Optional[int] = ...) -> None: ...
