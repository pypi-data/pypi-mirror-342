from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Schema(_message.Message):
    __slots__ = ["hash", "channel_name", "schema_text"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_TEXT_FIELD_NUMBER: _ClassVar[int]
    hash: int
    channel_name: str
    schema_text: str
    def __init__(self, hash: _Optional[int] = ..., channel_name: _Optional[str] = ..., schema_text: _Optional[str] = ...) -> None: ...
