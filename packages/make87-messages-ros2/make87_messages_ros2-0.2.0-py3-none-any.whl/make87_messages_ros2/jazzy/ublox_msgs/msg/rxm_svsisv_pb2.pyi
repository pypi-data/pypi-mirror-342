from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RxmSVSISV(_message.Message):
    __slots__ = ["svid", "sv_flag", "azim", "elev", "age"]
    SVID_FIELD_NUMBER: _ClassVar[int]
    SV_FLAG_FIELD_NUMBER: _ClassVar[int]
    AZIM_FIELD_NUMBER: _ClassVar[int]
    ELEV_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    svid: int
    sv_flag: int
    azim: int
    elev: int
    age: int
    def __init__(self, svid: _Optional[int] = ..., sv_flag: _Optional[int] = ..., azim: _Optional[int] = ..., elev: _Optional[int] = ..., age: _Optional[int] = ...) -> None: ...
