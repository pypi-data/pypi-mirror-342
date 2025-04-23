from make87_messages_ros2.jazzy.std_msgs.msg import float32_multi_array_pb2 as _float32_multi_array_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectsStamped(_message.Message):
    __slots__ = ["header", "objects"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    objects: _float32_multi_array_pb2.Float32MultiArray
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., objects: _Optional[_Union[_float32_multi_array_pb2.Float32MultiArray, _Mapping]] = ...) -> None: ...
