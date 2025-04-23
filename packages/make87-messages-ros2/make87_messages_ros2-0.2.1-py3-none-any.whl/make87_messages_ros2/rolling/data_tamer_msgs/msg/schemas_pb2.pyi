from make87_messages_ros2.rolling.data_tamer_msgs.msg import schema_pb2 as _schema_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Schemas(_message.Message):
    __slots__ = ["schemas"]
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    schemas: _containers.RepeatedCompositeFieldContainer[_schema_pb2.Schema]
    def __init__(self, schemas: _Optional[_Iterable[_Union[_schema_pb2.Schema, _Mapping]]] = ...) -> None: ...
