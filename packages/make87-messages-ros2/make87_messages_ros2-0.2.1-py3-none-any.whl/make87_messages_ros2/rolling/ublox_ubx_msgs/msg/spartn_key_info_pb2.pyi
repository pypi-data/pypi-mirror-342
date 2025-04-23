from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SpartnKeyInfo(_message.Message):
    __slots__ = ["reserved1", "key_length_bytes", "valid_from_wno", "valid_from_tow"]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    KEY_LENGTH_BYTES_FIELD_NUMBER: _ClassVar[int]
    VALID_FROM_WNO_FIELD_NUMBER: _ClassVar[int]
    VALID_FROM_TOW_FIELD_NUMBER: _ClassVar[int]
    reserved1: int
    key_length_bytes: int
    valid_from_wno: int
    valid_from_tow: int
    def __init__(self, reserved1: _Optional[int] = ..., key_length_bytes: _Optional[int] = ..., valid_from_wno: _Optional[int] = ..., valid_from_tow: _Optional[int] = ...) -> None: ...
