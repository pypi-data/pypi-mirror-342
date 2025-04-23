from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PersonalDataProcessor(_message.Message):
    __slots__ = ["header", "data_source_node", "user_friendly_source_name", "data_purpose", "path"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_NODE_FIELD_NUMBER: _ClassVar[int]
    USER_FRIENDLY_SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_PURPOSE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    data_source_node: str
    user_friendly_source_name: str
    data_purpose: str
    path: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., data_source_node: _Optional[str] = ..., user_friendly_source_name: _Optional[str] = ..., data_purpose: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...
