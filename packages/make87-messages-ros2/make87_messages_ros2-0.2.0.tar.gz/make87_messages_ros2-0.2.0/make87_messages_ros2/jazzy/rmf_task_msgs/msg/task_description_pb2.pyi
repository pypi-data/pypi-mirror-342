from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.rmf_task_msgs.msg import clean_pb2 as _clean_pb2
from make87_messages_ros2.jazzy.rmf_task_msgs.msg import delivery_pb2 as _delivery_pb2
from make87_messages_ros2.jazzy.rmf_task_msgs.msg import loop_pb2 as _loop_pb2
from make87_messages_ros2.jazzy.rmf_task_msgs.msg import priority_pb2 as _priority_pb2
from make87_messages_ros2.jazzy.rmf_task_msgs.msg import station_pb2 as _station_pb2
from make87_messages_ros2.jazzy.rmf_task_msgs.msg import task_type_pb2 as _task_type_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskDescription(_message.Message):
    __slots__ = ["start_time", "priority", "task_type", "station", "loop", "delivery", "clean"]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATION_FIELD_NUMBER: _ClassVar[int]
    LOOP_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_FIELD_NUMBER: _ClassVar[int]
    CLEAN_FIELD_NUMBER: _ClassVar[int]
    start_time: _time_pb2.Time
    priority: _priority_pb2.Priority
    task_type: _task_type_pb2.TaskType
    station: _station_pb2.Station
    loop: _loop_pb2.Loop
    delivery: _delivery_pb2.Delivery
    clean: _clean_pb2.Clean
    def __init__(self, start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., priority: _Optional[_Union[_priority_pb2.Priority, _Mapping]] = ..., task_type: _Optional[_Union[_task_type_pb2.TaskType, _Mapping]] = ..., station: _Optional[_Union[_station_pb2.Station, _Mapping]] = ..., loop: _Optional[_Union[_loop_pb2.Loop, _Mapping]] = ..., delivery: _Optional[_Union[_delivery_pb2.Delivery, _Mapping]] = ..., clean: _Optional[_Union[_clean_pb2.Clean, _Mapping]] = ...) -> None: ...
