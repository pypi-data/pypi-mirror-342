from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OtherOrbInfo(_message.Message):
    __slots__ = ["header", "ano_aop_usability", "orb_type"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ANO_AOP_USABILITY_FIELD_NUMBER: _ClassVar[int]
    ORB_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ano_aop_usability: int
    orb_type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ano_aop_usability: _Optional[int] = ..., orb_type: _Optional[int] = ...) -> None: ...
