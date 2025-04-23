from make87_messages_ros2.rolling.yasmin_msgs.msg import transition_pb2 as _transition_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class State(_message.Message):
    __slots__ = ["id", "parent", "name", "transitions", "outcomes", "is_fsm", "current_state"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    IS_FSM_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
    id: int
    parent: int
    name: str
    transitions: _containers.RepeatedCompositeFieldContainer[_transition_pb2.Transition]
    outcomes: _containers.RepeatedScalarFieldContainer[str]
    is_fsm: bool
    current_state: int
    def __init__(self, id: _Optional[int] = ..., parent: _Optional[int] = ..., name: _Optional[str] = ..., transitions: _Optional[_Iterable[_Union[_transition_pb2.Transition, _Mapping]]] = ..., outcomes: _Optional[_Iterable[str]] = ..., is_fsm: bool = ..., current_state: _Optional[int] = ...) -> None: ...
