from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RadarPreHeaderDeviceBlock(_message.Message):
    __slots__ = ["uiident", "udiserialno", "bdeviceerror", "bcontaminationwarning", "bcontaminationerror"]
    UIIDENT_FIELD_NUMBER: _ClassVar[int]
    UDISERIALNO_FIELD_NUMBER: _ClassVar[int]
    BDEVICEERROR_FIELD_NUMBER: _ClassVar[int]
    BCONTAMINATIONWARNING_FIELD_NUMBER: _ClassVar[int]
    BCONTAMINATIONERROR_FIELD_NUMBER: _ClassVar[int]
    uiident: int
    udiserialno: int
    bdeviceerror: bool
    bcontaminationwarning: bool
    bcontaminationerror: bool
    def __init__(self, uiident: _Optional[int] = ..., udiserialno: _Optional[int] = ..., bdeviceerror: bool = ..., bcontaminationwarning: bool = ..., bcontaminationerror: bool = ...) -> None: ...
