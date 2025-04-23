from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BlockadeCheckpoint(_message.Message):
    __slots__ = ["position", "map_name", "can_hold"]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    CAN_HOLD_FIELD_NUMBER: _ClassVar[int]
    position: _containers.RepeatedScalarFieldContainer[float]
    map_name: str
    can_hold: bool
    def __init__(self, position: _Optional[_Iterable[float]] = ..., map_name: _Optional[str] = ..., can_hold: bool = ...) -> None: ...
