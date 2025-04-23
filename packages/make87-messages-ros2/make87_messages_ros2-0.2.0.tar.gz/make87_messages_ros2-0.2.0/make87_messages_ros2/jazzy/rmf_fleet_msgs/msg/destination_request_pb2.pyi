from make87_messages_ros2.jazzy.rmf_fleet_msgs.msg import location_pb2 as _location_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DestinationRequest(_message.Message):
    __slots__ = ["fleet_name", "robot_name", "destination", "task_id"]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    fleet_name: str
    robot_name: str
    destination: _location_pb2.Location
    task_id: str
    def __init__(self, fleet_name: _Optional[str] = ..., robot_name: _Optional[str] = ..., destination: _Optional[_Union[_location_pb2.Location, _Mapping]] = ..., task_id: _Optional[str] = ...) -> None: ...
