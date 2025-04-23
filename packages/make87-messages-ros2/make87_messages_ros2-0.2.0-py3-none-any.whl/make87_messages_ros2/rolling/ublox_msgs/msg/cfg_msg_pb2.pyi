from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgMSG(_message.Message):
    __slots__ = ["msg_class", "msg_id", "rate"]
    MSG_CLASS_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    msg_class: int
    msg_id: int
    rate: int
    def __init__(self, msg_class: _Optional[int] = ..., msg_id: _Optional[int] = ..., rate: _Optional[int] = ...) -> None: ...
