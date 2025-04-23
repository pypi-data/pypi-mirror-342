from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.jazzy.vision_msgs.msg import object_hypothesis_pb2 as _object_hypothesis_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Classification(_message.Message):
    __slots__ = ["header", "results"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    results: _containers.RepeatedCompositeFieldContainer[_object_hypothesis_pb2.ObjectHypothesis]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., results: _Optional[_Iterable[_Union[_object_hypothesis_pb2.ObjectHypothesis, _Mapping]]] = ...) -> None: ...
