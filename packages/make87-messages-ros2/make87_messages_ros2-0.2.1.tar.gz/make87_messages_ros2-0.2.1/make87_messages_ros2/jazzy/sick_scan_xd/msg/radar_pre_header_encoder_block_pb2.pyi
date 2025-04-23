from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RadarPreHeaderEncoderBlock(_message.Message):
    __slots__ = ["udiencoderpos", "iencoderspeed"]
    UDIENCODERPOS_FIELD_NUMBER: _ClassVar[int]
    IENCODERSPEED_FIELD_NUMBER: _ClassVar[int]
    udiencoderpos: int
    iencoderspeed: int
    def __init__(self, udiencoderpos: _Optional[int] = ..., iencoderspeed: _Optional[int] = ...) -> None: ...
