from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ParamPullRequest(_message.Message):
    __slots__ = ["force_pull"]
    FORCE_PULL_FIELD_NUMBER: _ClassVar[int]
    force_pull: bool
    def __init__(self, force_pull: bool = ...) -> None: ...

class ParamPullResponse(_message.Message):
    __slots__ = ["success", "param_received"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    PARAM_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    success: bool
    param_received: int
    def __init__(self, success: bool = ..., param_received: _Optional[int] = ...) -> None: ...
