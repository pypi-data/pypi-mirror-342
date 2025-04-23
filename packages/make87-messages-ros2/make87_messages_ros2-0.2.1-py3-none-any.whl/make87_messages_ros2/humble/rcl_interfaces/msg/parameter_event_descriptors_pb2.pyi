from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rcl_interfaces.msg import parameter_descriptor_pb2 as _parameter_descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParameterEventDescriptors(_message.Message):
    __slots__ = ["header", "new_parameters", "changed_parameters", "deleted_parameters"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NEW_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    CHANGED_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    DELETED_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    new_parameters: _containers.RepeatedCompositeFieldContainer[_parameter_descriptor_pb2.ParameterDescriptor]
    changed_parameters: _containers.RepeatedCompositeFieldContainer[_parameter_descriptor_pb2.ParameterDescriptor]
    deleted_parameters: _containers.RepeatedCompositeFieldContainer[_parameter_descriptor_pb2.ParameterDescriptor]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., new_parameters: _Optional[_Iterable[_Union[_parameter_descriptor_pb2.ParameterDescriptor, _Mapping]]] = ..., changed_parameters: _Optional[_Iterable[_Union[_parameter_descriptor_pb2.ParameterDescriptor, _Mapping]]] = ..., deleted_parameters: _Optional[_Iterable[_Union[_parameter_descriptor_pb2.ParameterDescriptor, _Mapping]]] = ...) -> None: ...
