from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Switches(_message.Message):
    __slots__ = ["switch0", "switch1", "switch2"]
    SWITCH0_FIELD_NUMBER: _ClassVar[int]
    SWITCH1_FIELD_NUMBER: _ClassVar[int]
    SWITCH2_FIELD_NUMBER: _ClassVar[int]
    switch0: bool
    switch1: bool
    switch2: bool
    def __init__(self, switch0: bool = ..., switch1: bool = ..., switch2: bool = ...) -> None: ...
