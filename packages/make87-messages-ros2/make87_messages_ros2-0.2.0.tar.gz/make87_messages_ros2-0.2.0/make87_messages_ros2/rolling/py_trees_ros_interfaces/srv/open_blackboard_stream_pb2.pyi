from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OpenBlackboardStreamRequest(_message.Message):
    __slots__ = ["variables", "filter_on_visited_path", "with_activity_stream"]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    FILTER_ON_VISITED_PATH_FIELD_NUMBER: _ClassVar[int]
    WITH_ACTIVITY_STREAM_FIELD_NUMBER: _ClassVar[int]
    variables: _containers.RepeatedScalarFieldContainer[str]
    filter_on_visited_path: bool
    with_activity_stream: bool
    def __init__(self, variables: _Optional[_Iterable[str]] = ..., filter_on_visited_path: bool = ..., with_activity_stream: bool = ...) -> None: ...

class OpenBlackboardStreamResponse(_message.Message):
    __slots__ = ["topic"]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    topic: str
    def __init__(self, topic: _Optional[str] = ...) -> None: ...
