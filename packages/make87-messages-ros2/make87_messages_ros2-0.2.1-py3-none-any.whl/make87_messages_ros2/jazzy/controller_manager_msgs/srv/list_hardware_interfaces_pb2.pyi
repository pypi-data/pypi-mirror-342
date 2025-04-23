from make87_messages_ros2.jazzy.controller_manager_msgs.msg import hardware_interface_pb2 as _hardware_interface_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListHardwareInterfacesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListHardwareInterfacesResponse(_message.Message):
    __slots__ = ["command_interfaces", "state_interfaces"]
    COMMAND_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    STATE_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    command_interfaces: _containers.RepeatedCompositeFieldContainer[_hardware_interface_pb2.HardwareInterface]
    state_interfaces: _containers.RepeatedCompositeFieldContainer[_hardware_interface_pb2.HardwareInterface]
    def __init__(self, command_interfaces: _Optional[_Iterable[_Union[_hardware_interface_pb2.HardwareInterface, _Mapping]]] = ..., state_interfaces: _Optional[_Iterable[_Union[_hardware_interface_pb2.HardwareInterface, _Mapping]]] = ...) -> None: ...
