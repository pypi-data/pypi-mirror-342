from make87_messages_ros2.rolling.rmf_fleet_msgs.msg import dock_pb2 as _dock_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DockSummary(_message.Message):
    __slots__ = ["docks"]
    DOCKS_FIELD_NUMBER: _ClassVar[int]
    docks: _containers.RepeatedCompositeFieldContainer[_dock_pb2.Dock]
    def __init__(self, docks: _Optional[_Iterable[_Union[_dock_pb2.Dock, _Mapping]]] = ...) -> None: ...
