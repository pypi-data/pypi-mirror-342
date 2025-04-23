from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetCostRequest(_message.Message):
    __slots__ = ["use_footprint", "x", "y", "theta"]
    USE_FOOTPRINT_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    THETA_FIELD_NUMBER: _ClassVar[int]
    use_footprint: bool
    x: float
    y: float
    theta: float
    def __init__(self, use_footprint: bool = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., theta: _Optional[float] = ...) -> None: ...

class GetCostResponse(_message.Message):
    __slots__ = ["cost"]
    COST_FIELD_NUMBER: _ClassVar[int]
    cost: float
    def __init__(self, cost: _Optional[float] = ...) -> None: ...
