from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Tow(_message.Message):
    __slots__ = ["task_id", "object_type", "is_object_id_known", "object_id", "pickup_place_name", "is_dropoff_place_known", "dropoff_place_name"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_OBJECT_ID_KNOWN_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PICKUP_PLACE_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_DROPOFF_PLACE_KNOWN_FIELD_NUMBER: _ClassVar[int]
    DROPOFF_PLACE_NAME_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    object_type: str
    is_object_id_known: bool
    object_id: str
    pickup_place_name: str
    is_dropoff_place_known: bool
    dropoff_place_name: str
    def __init__(self, task_id: _Optional[str] = ..., object_type: _Optional[str] = ..., is_object_id_known: bool = ..., object_id: _Optional[str] = ..., pickup_place_name: _Optional[str] = ..., is_dropoff_place_known: bool = ..., dropoff_place_name: _Optional[str] = ...) -> None: ...
