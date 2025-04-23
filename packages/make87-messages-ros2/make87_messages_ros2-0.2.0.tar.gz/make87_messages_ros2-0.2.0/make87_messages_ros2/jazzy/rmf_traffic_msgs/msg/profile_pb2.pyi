from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import convex_shape_pb2 as _convex_shape_pb2
from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import convex_shape_context_pb2 as _convex_shape_context_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Profile(_message.Message):
    __slots__ = ["footprint", "vicinity", "shape_context"]
    FOOTPRINT_FIELD_NUMBER: _ClassVar[int]
    VICINITY_FIELD_NUMBER: _ClassVar[int]
    SHAPE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    footprint: _convex_shape_pb2.ConvexShape
    vicinity: _convex_shape_pb2.ConvexShape
    shape_context: _convex_shape_context_pb2.ConvexShapeContext
    def __init__(self, footprint: _Optional[_Union[_convex_shape_pb2.ConvexShape, _Mapping]] = ..., vicinity: _Optional[_Union[_convex_shape_pb2.ConvexShape, _Mapping]] = ..., shape_context: _Optional[_Union[_convex_shape_context_pb2.ConvexShapeContext, _Mapping]] = ...) -> None: ...
