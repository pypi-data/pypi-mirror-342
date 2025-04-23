from make87_messages_ros2.jazzy.autoware_perception_msgs.msg import traffic_signal_pb2 as _traffic_signal_pb2
from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrafficSignalArray(_message.Message):
    __slots__ = ["stamp", "signals"]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    SIGNALS_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    signals: _containers.RepeatedCompositeFieldContainer[_traffic_signal_pb2.TrafficSignal]
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., signals: _Optional[_Iterable[_Union[_traffic_signal_pb2.TrafficSignal, _Mapping]]] = ...) -> None: ...
