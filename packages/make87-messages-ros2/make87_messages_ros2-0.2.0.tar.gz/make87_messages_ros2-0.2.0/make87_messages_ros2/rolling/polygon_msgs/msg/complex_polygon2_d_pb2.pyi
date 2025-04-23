from make87_messages_ros2.rolling.polygon_msgs.msg import polygon2_d_pb2 as _polygon2_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ComplexPolygon2D(_message.Message):
    __slots__ = ["outer", "inner"]
    OUTER_FIELD_NUMBER: _ClassVar[int]
    INNER_FIELD_NUMBER: _ClassVar[int]
    outer: _polygon2_d_pb2.Polygon2D
    inner: _containers.RepeatedCompositeFieldContainer[_polygon2_d_pb2.Polygon2D]
    def __init__(self, outer: _Optional[_Union[_polygon2_d_pb2.Polygon2D, _Mapping]] = ..., inner: _Optional[_Iterable[_Union[_polygon2_d_pb2.Polygon2D, _Mapping]]] = ...) -> None: ...
