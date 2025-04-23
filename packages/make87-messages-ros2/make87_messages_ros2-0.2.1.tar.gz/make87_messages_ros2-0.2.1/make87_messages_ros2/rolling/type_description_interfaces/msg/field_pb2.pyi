from make87_messages_ros2.rolling.type_description_interfaces.msg import field_type_pb2 as _field_type_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Field(_message.Message):
    __slots__ = ["name", "type", "default_value"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: _field_type_pb2.FieldType
    default_value: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[_field_type_pb2.FieldType, _Mapping]] = ..., default_value: _Optional[str] = ...) -> None: ...
