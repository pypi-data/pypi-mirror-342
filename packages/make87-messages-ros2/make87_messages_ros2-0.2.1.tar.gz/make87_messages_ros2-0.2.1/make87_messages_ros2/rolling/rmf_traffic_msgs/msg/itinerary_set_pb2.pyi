from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import route_pb2 as _route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ItinerarySet(_message.Message):
    __slots__ = ["participant", "plan", "itinerary", "storage_base", "itinerary_version"]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_FIELD_NUMBER: _ClassVar[int]
    STORAGE_BASE_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_VERSION_FIELD_NUMBER: _ClassVar[int]
    participant: int
    plan: int
    itinerary: _containers.RepeatedCompositeFieldContainer[_route_pb2.Route]
    storage_base: int
    itinerary_version: int
    def __init__(self, participant: _Optional[int] = ..., plan: _Optional[int] = ..., itinerary: _Optional[_Iterable[_Union[_route_pb2.Route, _Mapping]]] = ..., storage_base: _Optional[int] = ..., itinerary_version: _Optional[int] = ...) -> None: ...
