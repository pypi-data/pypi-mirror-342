from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.std_msgs.msg import string_pb2 as _string_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScanMatchingStatus(_message.Message):
    __slots__ = ["header", "ros2_header", "has_converged", "matching_error", "inlier_fraction", "relative_pose", "prediction_labels", "prediction_errors"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    HAS_CONVERGED_FIELD_NUMBER: _ClassVar[int]
    MATCHING_ERROR_FIELD_NUMBER: _ClassVar[int]
    INLIER_FRACTION_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_POSE_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_LABELS_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_ERRORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    has_converged: bool
    matching_error: float
    inlier_fraction: float
    relative_pose: _pose_pb2.Pose
    prediction_labels: _containers.RepeatedCompositeFieldContainer[_string_pb2.String]
    prediction_errors: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., has_converged: bool = ..., matching_error: _Optional[float] = ..., inlier_fraction: _Optional[float] = ..., relative_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., prediction_labels: _Optional[_Iterable[_Union[_string_pb2.String, _Mapping]]] = ..., prediction_errors: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ...) -> None: ...
