from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Dictionary(_message.Message):
    __slots__ = ["dictionary_uuid", "names"]
    DICTIONARY_UUID_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    dictionary_uuid: int
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dictionary_uuid: _Optional[int] = ..., names: _Optional[_Iterable[str]] = ...) -> None: ...
