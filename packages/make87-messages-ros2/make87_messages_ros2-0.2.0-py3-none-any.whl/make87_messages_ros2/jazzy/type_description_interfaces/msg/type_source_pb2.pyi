from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TypeSource(_message.Message):
    __slots__ = ["type_name", "encoding", "raw_file_contents"]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    RAW_FILE_CONTENTS_FIELD_NUMBER: _ClassVar[int]
    type_name: str
    encoding: str
    raw_file_contents: str
    def __init__(self, type_name: _Optional[str] = ..., encoding: _Optional[str] = ..., raw_file_contents: _Optional[str] = ...) -> None: ...
