from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReportIndex(_message.Message):
    __slots__ = ["report_index"]
    REPORT_INDEX_FIELD_NUMBER: _ClassVar[int]
    report_index: int
    def __init__(self, report_index: _Optional[int] = ...) -> None: ...
