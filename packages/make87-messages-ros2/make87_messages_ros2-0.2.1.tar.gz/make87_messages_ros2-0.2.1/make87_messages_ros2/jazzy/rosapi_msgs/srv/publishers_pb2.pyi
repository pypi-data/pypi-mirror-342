from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PublishersRequest(_message.Message):
    __slots__ = ["topic"]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    topic: str
    def __init__(self, topic: _Optional[str] = ...) -> None: ...

class PublishersResponse(_message.Message):
    __slots__ = ["publishers"]
    PUBLISHERS_FIELD_NUMBER: _ClassVar[int]
    publishers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, publishers: _Optional[_Iterable[str]] = ...) -> None: ...
