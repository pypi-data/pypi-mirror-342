from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marti_common_msgs.msg import key_value_pb2 as _key_value_pb2
from make87_messages_ros2.humble.marti_nav_msgs.msg import route_pb2 as _route_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RouteArray(_message.Message):
    __slots__ = ["header", "ros2_header", "routes", "properties"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    routes: _containers.RepeatedCompositeFieldContainer[_route_pb2.Route]
    properties: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., routes: _Optional[_Iterable[_Union[_route_pb2.Route, _Mapping]]] = ..., properties: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
