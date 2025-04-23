from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChargerState(_message.Message):
    __slots__ = ["charger_time", "state", "charger_name", "error_message", "request_id", "robot_fleet", "robot_name", "time_to_fully_charged"]
    CHARGER_TIME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CHARGER_NAME_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FLEET_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_TO_FULLY_CHARGED_FIELD_NUMBER: _ClassVar[int]
    charger_time: _time_pb2.Time
    state: int
    charger_name: str
    error_message: str
    request_id: str
    robot_fleet: str
    robot_name: str
    time_to_fully_charged: _duration_pb2.Duration
    def __init__(self, charger_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., state: _Optional[int] = ..., charger_name: _Optional[str] = ..., error_message: _Optional[str] = ..., request_id: _Optional[str] = ..., robot_fleet: _Optional[str] = ..., robot_name: _Optional[str] = ..., time_to_fully_charged: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
