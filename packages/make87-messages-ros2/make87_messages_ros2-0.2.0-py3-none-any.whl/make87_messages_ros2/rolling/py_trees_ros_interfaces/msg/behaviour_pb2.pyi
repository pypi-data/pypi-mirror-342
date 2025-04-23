from make87_messages_ros2.rolling.py_trees_ros_interfaces.msg import key_value_pb2 as _key_value_pb2
from make87_messages_ros2.rolling.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Behaviour(_message.Message):
    __slots__ = ["name", "class_name", "own_id", "parent_id", "tip_id", "child_ids", "current_child_id", "type", "additional_detail", "blackbox_level", "status", "message", "is_active", "blackboard_access"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    OWN_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    TIP_ID_FIELD_NUMBER: _ClassVar[int]
    CHILD_IDS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_CHILD_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_DETAIL_FIELD_NUMBER: _ClassVar[int]
    BLACKBOX_LEVEL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    BLACKBOARD_ACCESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    class_name: str
    own_id: _uuid_pb2.UUID
    parent_id: _uuid_pb2.UUID
    tip_id: _uuid_pb2.UUID
    child_ids: _containers.RepeatedCompositeFieldContainer[_uuid_pb2.UUID]
    current_child_id: _uuid_pb2.UUID
    type: int
    additional_detail: str
    blackbox_level: int
    status: int
    message: str
    is_active: bool
    blackboard_access: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, name: _Optional[str] = ..., class_name: _Optional[str] = ..., own_id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., parent_id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., tip_id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., child_ids: _Optional[_Iterable[_Union[_uuid_pb2.UUID, _Mapping]]] = ..., current_child_id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., type: _Optional[int] = ..., additional_detail: _Optional[str] = ..., blackbox_level: _Optional[int] = ..., status: _Optional[int] = ..., message: _Optional[str] = ..., is_active: bool = ..., blackboard_access: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
