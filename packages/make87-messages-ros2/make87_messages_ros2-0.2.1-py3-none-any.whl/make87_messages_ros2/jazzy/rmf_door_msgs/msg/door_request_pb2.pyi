from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.rmf_door_msgs.msg import door_mode_pb2 as _door_mode_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DoorRequest(_message.Message):
    __slots__ = ["request_time", "requester_id", "door_name", "requested_mode"]
    REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    REQUESTER_ID_FIELD_NUMBER: _ClassVar[int]
    DOOR_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_MODE_FIELD_NUMBER: _ClassVar[int]
    request_time: _time_pb2.Time
    requester_id: str
    door_name: str
    requested_mode: _door_mode_pb2.DoorMode
    def __init__(self, request_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., requester_id: _Optional[str] = ..., door_name: _Optional[str] = ..., requested_mode: _Optional[_Union[_door_mode_pb2.DoorMode, _Mapping]] = ...) -> None: ...
