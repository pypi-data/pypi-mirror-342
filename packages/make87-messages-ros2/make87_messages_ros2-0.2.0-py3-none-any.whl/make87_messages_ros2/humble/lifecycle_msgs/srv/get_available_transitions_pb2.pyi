from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.lifecycle_msgs.msg import transition_description_pb2 as _transition_description_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetAvailableTransitionsRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetAvailableTransitionsResponse(_message.Message):
    __slots__ = ["header", "available_transitions"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    available_transitions: _containers.RepeatedCompositeFieldContainer[_transition_description_pb2.TransitionDescription]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., available_transitions: _Optional[_Iterable[_Union[_transition_description_pb2.TransitionDescription, _Mapping]]] = ...) -> None: ...
