from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.data_tamer_msgs.msg import schema_pb2 as _schema_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Schemas(_message.Message):
    __slots__ = ["header", "schemas"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    schemas: _containers.RepeatedCompositeFieldContainer[_schema_pb2.Schema]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., schemas: _Optional[_Iterable[_Union[_schema_pb2.Schema, _Mapping]]] = ...) -> None: ...
