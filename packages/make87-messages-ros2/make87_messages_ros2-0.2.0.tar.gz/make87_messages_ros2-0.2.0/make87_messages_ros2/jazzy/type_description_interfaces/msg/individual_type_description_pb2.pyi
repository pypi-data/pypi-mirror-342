from make87_messages_ros2.jazzy.type_description_interfaces.msg import field_pb2 as _field_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IndividualTypeDescription(_message.Message):
    __slots__ = ["type_name", "fields"]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    type_name: str
    fields: _containers.RepeatedCompositeFieldContainer[_field_pb2.Field]
    def __init__(self, type_name: _Optional[str] = ..., fields: _Optional[_Iterable[_Union[_field_pb2.Field, _Mapping]]] = ...) -> None: ...
