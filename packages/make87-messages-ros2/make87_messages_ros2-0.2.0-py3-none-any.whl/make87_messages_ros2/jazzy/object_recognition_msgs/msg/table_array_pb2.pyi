from make87_messages_ros2.jazzy.object_recognition_msgs.msg import table_pb2 as _table_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TableArray(_message.Message):
    __slots__ = ["header", "tables"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    tables: _containers.RepeatedCompositeFieldContainer[_table_pb2.Table]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., tables: _Optional[_Iterable[_Union[_table_pb2.Table, _Mapping]]] = ...) -> None: ...
