from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import planner_interface_description_pb2 as _planner_interface_description_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryPlannerInterfacesRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class QueryPlannerInterfacesResponse(_message.Message):
    __slots__ = ["header", "planner_interfaces"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PLANNER_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    planner_interfaces: _containers.RepeatedCompositeFieldContainer[_planner_interface_description_pb2.PlannerInterfaceDescription]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., planner_interfaces: _Optional[_Iterable[_Union[_planner_interface_description_pb2.PlannerInterfaceDescription, _Mapping]]] = ...) -> None: ...
