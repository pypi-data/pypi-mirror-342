from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_multi_robot_msgs.msg import station_pb2 as _station_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Order(_message.Message):
    __slots__ = ["header", "order_id", "order_name", "stations"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_NAME_FIELD_NUMBER: _ClassVar[int]
    STATIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    order_id: int
    order_name: str
    stations: _containers.RepeatedCompositeFieldContainer[_station_pb2.Station]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., order_id: _Optional[int] = ..., order_name: _Optional[str] = ..., stations: _Optional[_Iterable[_Union[_station_pb2.Station, _Mapping]]] = ...) -> None: ...
