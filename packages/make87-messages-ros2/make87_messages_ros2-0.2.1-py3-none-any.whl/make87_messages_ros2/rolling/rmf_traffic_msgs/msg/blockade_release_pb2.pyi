from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BlockadeRelease(_message.Message):
    __slots__ = ["participant", "reservation", "checkpoint"]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    participant: int
    reservation: int
    checkpoint: int
    def __init__(self, participant: _Optional[int] = ..., reservation: _Optional[int] = ..., checkpoint: _Optional[int] = ...) -> None: ...
