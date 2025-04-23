from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetExposureRequest(_message.Message):
    __slots__ = ["auto_exposure", "time"]
    AUTO_EXPOSURE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    auto_exposure: bool
    time: int
    def __init__(self, auto_exposure: bool = ..., time: _Optional[int] = ...) -> None: ...

class SetExposureResponse(_message.Message):
    __slots__ = ["auto_exposure", "time"]
    AUTO_EXPOSURE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    auto_exposure: bool
    time: int
    def __init__(self, auto_exposure: bool = ..., time: _Optional[int] = ...) -> None: ...
