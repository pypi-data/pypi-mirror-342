from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetMavFrameRequest(_message.Message):
    __slots__ = ["mav_frame"]
    MAV_FRAME_FIELD_NUMBER: _ClassVar[int]
    mav_frame: int
    def __init__(self, mav_frame: _Optional[int] = ...) -> None: ...

class SetMavFrameResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
