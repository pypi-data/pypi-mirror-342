from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SwitchControllerRequest(_message.Message):
    __slots__ = ["activate_controllers", "deactivate_controllers", "strictness", "activate_asap", "timeout"]
    ACTIVATE_CONTROLLERS_FIELD_NUMBER: _ClassVar[int]
    DEACTIVATE_CONTROLLERS_FIELD_NUMBER: _ClassVar[int]
    STRICTNESS_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_ASAP_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    activate_controllers: _containers.RepeatedScalarFieldContainer[str]
    deactivate_controllers: _containers.RepeatedScalarFieldContainer[str]
    strictness: int
    activate_asap: bool
    timeout: _duration_pb2.Duration
    def __init__(self, activate_controllers: _Optional[_Iterable[str]] = ..., deactivate_controllers: _Optional[_Iterable[str]] = ..., strictness: _Optional[int] = ..., activate_asap: bool = ..., timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class SwitchControllerResponse(_message.Message):
    __slots__ = ["ok"]
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...
