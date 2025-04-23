from make87_messages_ros2.rolling.lifecycle_msgs.msg import transition_description_pb2 as _transition_description_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetAvailableTransitionsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetAvailableTransitionsResponse(_message.Message):
    __slots__ = ["available_transitions"]
    AVAILABLE_TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    available_transitions: _containers.RepeatedCompositeFieldContainer[_transition_description_pb2.TransitionDescription]
    def __init__(self, available_transitions: _Optional[_Iterable[_Union[_transition_description_pb2.TransitionDescription, _Mapping]]] = ...) -> None: ...
