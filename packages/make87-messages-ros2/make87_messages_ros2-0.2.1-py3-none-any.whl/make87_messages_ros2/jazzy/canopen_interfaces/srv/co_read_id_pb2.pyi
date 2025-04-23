from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class COReadIDRequest(_message.Message):
    __slots__ = ["nodeid", "index", "subindex", "canopen_datatype"]
    NODEID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SUBINDEX_FIELD_NUMBER: _ClassVar[int]
    CANOPEN_DATATYPE_FIELD_NUMBER: _ClassVar[int]
    nodeid: int
    index: int
    subindex: int
    canopen_datatype: int
    def __init__(self, nodeid: _Optional[int] = ..., index: _Optional[int] = ..., subindex: _Optional[int] = ..., canopen_datatype: _Optional[int] = ...) -> None: ...

class COReadIDResponse(_message.Message):
    __slots__ = ["success", "data"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    data: int
    def __init__(self, success: bool = ..., data: _Optional[int] = ...) -> None: ...
