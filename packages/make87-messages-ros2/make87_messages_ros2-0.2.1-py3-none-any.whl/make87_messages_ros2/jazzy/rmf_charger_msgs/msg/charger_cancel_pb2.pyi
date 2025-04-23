from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChargerCancel(_message.Message):
    __slots__ = ["charger_name", "request_id"]
    CHARGER_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    charger_name: str
    request_id: str
    def __init__(self, charger_name: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...
