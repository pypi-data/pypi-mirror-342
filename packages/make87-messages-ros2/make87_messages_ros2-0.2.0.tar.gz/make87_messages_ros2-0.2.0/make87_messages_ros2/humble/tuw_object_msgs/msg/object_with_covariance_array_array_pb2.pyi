from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.tuw_object_msgs.msg import object_with_covariance_array_pb2 as _object_with_covariance_array_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectWithCovarianceArrayArray(_message.Message):
    __slots__ = ["header", "ros2_header", "objects_array"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_ARRAY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    objects_array: _containers.RepeatedCompositeFieldContainer[_object_with_covariance_array_pb2.ObjectWithCovarianceArray]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., objects_array: _Optional[_Iterable[_Union[_object_with_covariance_array_pb2.ObjectWithCovarianceArray, _Mapping]]] = ...) -> None: ...
