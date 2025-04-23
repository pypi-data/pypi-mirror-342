from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectClassification(_message.Message):
    __slots__ = ["header", "label", "probability"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    label: int
    probability: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., label: _Optional[int] = ..., probability: _Optional[float] = ...) -> None: ...
