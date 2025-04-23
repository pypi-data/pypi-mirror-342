from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CommandAckRequest(_message.Message):
    __slots__ = ["command", "result", "progress", "result_param2"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_PARAM2_FIELD_NUMBER: _ClassVar[int]
    command: int
    result: int
    progress: int
    result_param2: int
    def __init__(self, command: _Optional[int] = ..., result: _Optional[int] = ..., progress: _Optional[int] = ..., result_param2: _Optional[int] = ...) -> None: ...

class CommandAckResponse(_message.Message):
    __slots__ = ["success", "result"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: int
    def __init__(self, success: bool = ..., result: _Optional[int] = ...) -> None: ...
