from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import region_pb2 as _region_pb2
from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import shape_context_pb2 as _shape_context_pb2
from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import timespan_pb2 as _timespan_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleQuerySpacetime(_message.Message):
    __slots__ = ["type", "regions", "shape_context", "timespan"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    REGIONS_FIELD_NUMBER: _ClassVar[int]
    SHAPE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    TIMESPAN_FIELD_NUMBER: _ClassVar[int]
    type: int
    regions: _containers.RepeatedCompositeFieldContainer[_region_pb2.Region]
    shape_context: _shape_context_pb2.ShapeContext
    timespan: _timespan_pb2.Timespan
    def __init__(self, type: _Optional[int] = ..., regions: _Optional[_Iterable[_Union[_region_pb2.Region, _Mapping]]] = ..., shape_context: _Optional[_Union[_shape_context_pb2.ShapeContext, _Mapping]] = ..., timespan: _Optional[_Union[_timespan_pb2.Timespan, _Mapping]] = ...) -> None: ...
