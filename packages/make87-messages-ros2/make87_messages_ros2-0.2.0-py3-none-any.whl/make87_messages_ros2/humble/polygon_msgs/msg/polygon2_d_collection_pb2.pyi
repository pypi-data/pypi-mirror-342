from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.polygon_msgs.msg import polygon2_d_pb2 as _polygon2_d_pb2
from make87_messages_ros2.humble.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Polygon2DCollection(_message.Message):
    __slots__ = ["header", "ros2_header", "polygons", "colors"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    POLYGONS_FIELD_NUMBER: _ClassVar[int]
    COLORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    polygons: _containers.RepeatedCompositeFieldContainer[_polygon2_d_pb2.Polygon2D]
    colors: _containers.RepeatedCompositeFieldContainer[_color_rgba_pb2.ColorRGBA]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., polygons: _Optional[_Iterable[_Union[_polygon2_d_pb2.Polygon2D, _Mapping]]] = ..., colors: _Optional[_Iterable[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]]] = ...) -> None: ...
