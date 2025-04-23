from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PauseRequest(_message.Message):
    __slots__ = ["fleet_name", "robot_name", "mode_request_id", "type", "at_checkpoint"]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    MODE_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    AT_CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    fleet_name: str
    robot_name: str
    mode_request_id: int
    type: int
    at_checkpoint: int
    def __init__(self, fleet_name: _Optional[str] = ..., robot_name: _Optional[str] = ..., mode_request_id: _Optional[int] = ..., type: _Optional[int] = ..., at_checkpoint: _Optional[int] = ...) -> None: ...
