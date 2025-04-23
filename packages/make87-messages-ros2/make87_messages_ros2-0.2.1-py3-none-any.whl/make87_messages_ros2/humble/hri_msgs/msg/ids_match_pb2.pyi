from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IdsMatch(_message.Message):
    __slots__ = ["header", "id1", "id1_type", "id2", "id2_type", "confidence"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID1_FIELD_NUMBER: _ClassVar[int]
    ID1_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID2_FIELD_NUMBER: _ClassVar[int]
    ID2_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id1: str
    id1_type: int
    id2: str
    id2_type: int
    confidence: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id1: _Optional[str] = ..., id1_type: _Optional[int] = ..., id2: _Optional[str] = ..., id2_type: _Optional[int] = ..., confidence: _Optional[float] = ...) -> None: ...
