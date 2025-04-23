from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import box_pb2 as _box_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import rectangle_pb2 as _rectangle_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadCarrierModel(_message.Message):
    __slots__ = ["id", "type", "outer_dimensions", "inner_dimensions", "rim_thickness", "rim_step_height", "rim_ledge", "height_open_side", "pose", "pose_type"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTER_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    INNER_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    RIM_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    RIM_STEP_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    RIM_LEDGE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_OPEN_SIDE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    POSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    outer_dimensions: _box_pb2.Box
    inner_dimensions: _box_pb2.Box
    rim_thickness: _rectangle_pb2.Rectangle
    rim_step_height: float
    rim_ledge: _rectangle_pb2.Rectangle
    height_open_side: float
    pose: _pose_stamped_pb2.PoseStamped
    pose_type: str
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., outer_dimensions: _Optional[_Union[_box_pb2.Box, _Mapping]] = ..., inner_dimensions: _Optional[_Union[_box_pb2.Box, _Mapping]] = ..., rim_thickness: _Optional[_Union[_rectangle_pb2.Rectangle, _Mapping]] = ..., rim_step_height: _Optional[float] = ..., rim_ledge: _Optional[_Union[_rectangle_pb2.Rectangle, _Mapping]] = ..., height_open_side: _Optional[float] = ..., pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., pose_type: _Optional[str] = ...) -> None: ...
