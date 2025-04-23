from make87_messages_ros2.jazzy.autoware_control_msgs.msg import lateral_pb2 as _lateral_pb2
from make87_messages_ros2.jazzy.autoware_control_msgs.msg import longitudinal_pb2 as _longitudinal_pb2
from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Control(_message.Message):
    __slots__ = ["stamp", "control_time", "lateral", "longitudinal"]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    CONTROL_TIME_FIELD_NUMBER: _ClassVar[int]
    LATERAL_FIELD_NUMBER: _ClassVar[int]
    LONGITUDINAL_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    control_time: _time_pb2.Time
    lateral: _lateral_pb2.Lateral
    longitudinal: _longitudinal_pb2.Longitudinal
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., control_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., lateral: _Optional[_Union[_lateral_pb2.Lateral, _Mapping]] = ..., longitudinal: _Optional[_Union[_longitudinal_pb2.Longitudinal, _Mapping]] = ...) -> None: ...
