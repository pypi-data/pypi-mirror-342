from make87_messages_ros2.jazzy.std_msgs.msg import string_pb2 as _string_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SaveMapRequest(_message.Message):
    __slots__ = ["filename"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    filename: _string_pb2.String
    def __init__(self, filename: _Optional[_Union[_string_pb2.String, _Mapping]] = ...) -> None: ...

class SaveMapResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
