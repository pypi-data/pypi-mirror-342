from make87_messages_ros2.rolling.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SuctionGrasp(_message.Message):
    __slots__ = ["uuid", "item_uuid", "pose", "quality", "max_suction_surface_length", "max_suction_surface_width"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    ITEM_UUID_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    MAX_SUCTION_SURFACE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_SUCTION_SURFACE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    item_uuid: str
    pose: _pose_stamped_pb2.PoseStamped
    quality: float
    max_suction_surface_length: float
    max_suction_surface_width: float
    def __init__(self, uuid: _Optional[str] = ..., item_uuid: _Optional[str] = ..., pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., quality: _Optional[float] = ..., max_suction_surface_length: _Optional[float] = ..., max_suction_surface_width: _Optional[float] = ...) -> None: ...
