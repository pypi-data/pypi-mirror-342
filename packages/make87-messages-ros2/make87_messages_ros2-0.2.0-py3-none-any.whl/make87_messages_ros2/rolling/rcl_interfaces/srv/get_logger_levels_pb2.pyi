from make87_messages_ros2.rolling.rcl_interfaces.msg import logger_level_pb2 as _logger_level_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetLoggerLevelsRequest(_message.Message):
    __slots__ = ["names"]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: _Optional[_Iterable[str]] = ...) -> None: ...

class GetLoggerLevelsResponse(_message.Message):
    __slots__ = ["levels"]
    LEVELS_FIELD_NUMBER: _ClassVar[int]
    levels: _containers.RepeatedCompositeFieldContainer[_logger_level_pb2.LoggerLevel]
    def __init__(self, levels: _Optional[_Iterable[_Union[_logger_level_pb2.LoggerLevel, _Mapping]]] = ...) -> None: ...
