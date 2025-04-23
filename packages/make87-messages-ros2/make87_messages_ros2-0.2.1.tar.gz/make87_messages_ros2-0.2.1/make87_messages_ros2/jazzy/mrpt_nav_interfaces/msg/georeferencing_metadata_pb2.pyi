from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeoreferencingMetadata(_message.Message):
    __slots__ = ["valid", "t_enu_to_map", "t_enu_to_utm", "latitude", "longitude", "height", "utm_zone", "utm_band"]
    VALID_FIELD_NUMBER: _ClassVar[int]
    T_ENU_TO_MAP_FIELD_NUMBER: _ClassVar[int]
    T_ENU_TO_UTM_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    UTM_ZONE_FIELD_NUMBER: _ClassVar[int]
    UTM_BAND_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    t_enu_to_map: _pose_with_covariance_pb2.PoseWithCovariance
    t_enu_to_utm: _pose_pb2.Pose
    latitude: float
    longitude: float
    height: float
    utm_zone: int
    utm_band: str
    def __init__(self, valid: bool = ..., t_enu_to_map: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ..., t_enu_to_utm: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., height: _Optional[float] = ..., utm_zone: _Optional[int] = ..., utm_band: _Optional[str] = ...) -> None: ...
