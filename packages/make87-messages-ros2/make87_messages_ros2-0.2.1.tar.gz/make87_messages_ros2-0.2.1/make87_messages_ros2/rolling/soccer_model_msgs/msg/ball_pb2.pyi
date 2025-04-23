from make87_messages_ros2.rolling.geometry_msgs.msg import twist_with_covariance_pb2 as _twist_with_covariance_pb2
from make87_messages_ros2.rolling.soccer_geometry_msgs.msg import point_with_covariance_pb2 as _point_with_covariance_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ball(_message.Message):
    __slots__ = ["header", "point", "twist"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    point: _point_with_covariance_pb2.PointWithCovariance
    twist: _twist_with_covariance_pb2.TwistWithCovariance
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., point: _Optional[_Union[_point_with_covariance_pb2.PointWithCovariance, _Mapping]] = ..., twist: _Optional[_Union[_twist_with_covariance_pb2.TwistWithCovariance, _Mapping]] = ...) -> None: ...
