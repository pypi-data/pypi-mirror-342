from make87_messages_ros2.rolling.rcl_interfaces.msg import parameter_descriptor_pb2 as _parameter_descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DescribeParametersRequest(_message.Message):
    __slots__ = ["names"]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: _Optional[_Iterable[str]] = ...) -> None: ...

class DescribeParametersResponse(_message.Message):
    __slots__ = ["descriptors"]
    DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    descriptors: _containers.RepeatedCompositeFieldContainer[_parameter_descriptor_pb2.ParameterDescriptor]
    def __init__(self, descriptors: _Optional[_Iterable[_Union[_parameter_descriptor_pb2.ParameterDescriptor, _Mapping]]] = ...) -> None: ...
