from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OtherOrbInfo(_message.Message):
    __slots__ = ["ano_aop_usability", "orb_type"]
    ANO_AOP_USABILITY_FIELD_NUMBER: _ClassVar[int]
    ORB_TYPE_FIELD_NUMBER: _ClassVar[int]
    ano_aop_usability: int
    orb_type: int
    def __init__(self, ano_aop_usability: _Optional[int] = ..., orb_type: _Optional[int] = ...) -> None: ...
