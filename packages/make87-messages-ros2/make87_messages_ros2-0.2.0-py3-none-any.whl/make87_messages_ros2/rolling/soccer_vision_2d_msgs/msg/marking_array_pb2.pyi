from make87_messages_ros2.rolling.soccer_vision_2d_msgs.msg import marking_ellipse_pb2 as _marking_ellipse_pb2
from make87_messages_ros2.rolling.soccer_vision_2d_msgs.msg import marking_intersection_pb2 as _marking_intersection_pb2
from make87_messages_ros2.rolling.soccer_vision_2d_msgs.msg import marking_segment_pb2 as _marking_segment_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkingArray(_message.Message):
    __slots__ = ["header", "ellipses", "intersections", "segments"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ELLIPSES_FIELD_NUMBER: _ClassVar[int]
    INTERSECTIONS_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ellipses: _containers.RepeatedCompositeFieldContainer[_marking_ellipse_pb2.MarkingEllipse]
    intersections: _containers.RepeatedCompositeFieldContainer[_marking_intersection_pb2.MarkingIntersection]
    segments: _containers.RepeatedCompositeFieldContainer[_marking_segment_pb2.MarkingSegment]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ellipses: _Optional[_Iterable[_Union[_marking_ellipse_pb2.MarkingEllipse, _Mapping]]] = ..., intersections: _Optional[_Iterable[_Union[_marking_intersection_pb2.MarkingIntersection, _Mapping]]] = ..., segments: _Optional[_Iterable[_Union[_marking_segment_pb2.MarkingSegment, _Mapping]]] = ...) -> None: ...
