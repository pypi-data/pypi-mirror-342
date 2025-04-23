from make87_messages_ros2.rolling.autoware_perception_msgs.msg import predicted_path_pb2 as _predicted_path_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import accel_with_covariance_pb2 as _accel_with_covariance_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import twist_with_covariance_pb2 as _twist_with_covariance_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PredictedObjectKinematics(_message.Message):
    __slots__ = ["initial_pose_with_covariance", "initial_twist_with_covariance", "initial_acceleration_with_covariance", "predicted_paths"]
    INITIAL_POSE_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_TWIST_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_ACCELERATION_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    PREDICTED_PATHS_FIELD_NUMBER: _ClassVar[int]
    initial_pose_with_covariance: _pose_with_covariance_pb2.PoseWithCovariance
    initial_twist_with_covariance: _twist_with_covariance_pb2.TwistWithCovariance
    initial_acceleration_with_covariance: _accel_with_covariance_pb2.AccelWithCovariance
    predicted_paths: _containers.RepeatedCompositeFieldContainer[_predicted_path_pb2.PredictedPath]
    def __init__(self, initial_pose_with_covariance: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ..., initial_twist_with_covariance: _Optional[_Union[_twist_with_covariance_pb2.TwistWithCovariance, _Mapping]] = ..., initial_acceleration_with_covariance: _Optional[_Union[_accel_with_covariance_pb2.AccelWithCovariance, _Mapping]] = ..., predicted_paths: _Optional[_Iterable[_Union[_predicted_path_pb2.PredictedPath, _Mapping]]] = ...) -> None: ...
