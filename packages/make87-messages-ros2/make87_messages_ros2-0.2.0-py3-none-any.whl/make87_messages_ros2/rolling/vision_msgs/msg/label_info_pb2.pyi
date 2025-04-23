from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.vision_msgs.msg import vision_class_pb2 as _vision_class_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LabelInfo(_message.Message):
    __slots__ = ["header", "class_map", "threshold"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CLASS_MAP_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    class_map: _containers.RepeatedCompositeFieldContainer[_vision_class_pb2.VisionClass]
    threshold: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., class_map: _Optional[_Iterable[_Union[_vision_class_pb2.VisionClass, _Mapping]]] = ..., threshold: _Optional[float] = ...) -> None: ...
