from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import transform_pb2 as _transform_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import camera_models_pb2 as _camera_models_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import key_point_pb2 as _key_point_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import point2f_pb2 as _point2f_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import point3f_pb2 as _point3f_pb2
from make87_messages_ros2.jazzy.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OdomInfo(_message.Message):
    __slots__ = ["header", "lost", "matches", "inliers", "icp_inliers_ratio", "icp_rotation", "icp_translation", "icp_structural_complexity", "icp_structural_distribution", "icp_correspondences", "covariance", "features", "local_map_size", "local_scan_map_size", "local_key_frames", "local_bundle_outliers", "local_bundle_constraints", "local_bundle_time", "key_frame_added", "time_estimation", "time_particle_filtering", "stamp", "interval", "distance_travelled", "memory_usage", "gravity_roll_error", "gravity_pitch_error", "local_bundle_ids", "local_bundle_models", "local_bundle_poses", "transform", "transform_filtered", "transform_ground_truth", "guess", "type", "words_keys", "words_values", "word_matches", "word_inliers", "local_map_keys", "local_map_values", "local_scan_map", "ref_corners", "new_corners", "corner_inliers"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LOST_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    INLIERS_FIELD_NUMBER: _ClassVar[int]
    ICP_INLIERS_RATIO_FIELD_NUMBER: _ClassVar[int]
    ICP_ROTATION_FIELD_NUMBER: _ClassVar[int]
    ICP_TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    ICP_STRUCTURAL_COMPLEXITY_FIELD_NUMBER: _ClassVar[int]
    ICP_STRUCTURAL_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    ICP_CORRESPONDENCES_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    LOCAL_MAP_SIZE_FIELD_NUMBER: _ClassVar[int]
    LOCAL_SCAN_MAP_SIZE_FIELD_NUMBER: _ClassVar[int]
    LOCAL_KEY_FRAMES_FIELD_NUMBER: _ClassVar[int]
    LOCAL_BUNDLE_OUTLIERS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_BUNDLE_CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_BUNDLE_TIME_FIELD_NUMBER: _ClassVar[int]
    KEY_FRAME_ADDED_FIELD_NUMBER: _ClassVar[int]
    TIME_ESTIMATION_FIELD_NUMBER: _ClassVar[int]
    TIME_PARTICLE_FILTERING_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TRAVELLED_FIELD_NUMBER: _ClassVar[int]
    MEMORY_USAGE_FIELD_NUMBER: _ClassVar[int]
    GRAVITY_ROLL_ERROR_FIELD_NUMBER: _ClassVar[int]
    GRAVITY_PITCH_ERROR_FIELD_NUMBER: _ClassVar[int]
    LOCAL_BUNDLE_IDS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_BUNDLE_MODELS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_BUNDLE_POSES_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FILTERED_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_GROUND_TRUTH_FIELD_NUMBER: _ClassVar[int]
    GUESS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    WORDS_KEYS_FIELD_NUMBER: _ClassVar[int]
    WORDS_VALUES_FIELD_NUMBER: _ClassVar[int]
    WORD_MATCHES_FIELD_NUMBER: _ClassVar[int]
    WORD_INLIERS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_MAP_KEYS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_MAP_VALUES_FIELD_NUMBER: _ClassVar[int]
    LOCAL_SCAN_MAP_FIELD_NUMBER: _ClassVar[int]
    REF_CORNERS_FIELD_NUMBER: _ClassVar[int]
    NEW_CORNERS_FIELD_NUMBER: _ClassVar[int]
    CORNER_INLIERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    lost: bool
    matches: int
    inliers: int
    icp_inliers_ratio: float
    icp_rotation: float
    icp_translation: float
    icp_structural_complexity: float
    icp_structural_distribution: float
    icp_correspondences: int
    covariance: _containers.RepeatedScalarFieldContainer[float]
    features: int
    local_map_size: int
    local_scan_map_size: int
    local_key_frames: int
    local_bundle_outliers: int
    local_bundle_constraints: int
    local_bundle_time: float
    key_frame_added: bool
    time_estimation: float
    time_particle_filtering: float
    stamp: float
    interval: float
    distance_travelled: float
    memory_usage: int
    gravity_roll_error: float
    gravity_pitch_error: float
    local_bundle_ids: _containers.RepeatedScalarFieldContainer[int]
    local_bundle_models: _containers.RepeatedCompositeFieldContainer[_camera_models_pb2.CameraModels]
    local_bundle_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    transform: _transform_pb2.Transform
    transform_filtered: _transform_pb2.Transform
    transform_ground_truth: _transform_pb2.Transform
    guess: _transform_pb2.Transform
    type: int
    words_keys: _containers.RepeatedScalarFieldContainer[int]
    words_values: _containers.RepeatedCompositeFieldContainer[_key_point_pb2.KeyPoint]
    word_matches: _containers.RepeatedScalarFieldContainer[int]
    word_inliers: _containers.RepeatedScalarFieldContainer[int]
    local_map_keys: _containers.RepeatedScalarFieldContainer[int]
    local_map_values: _containers.RepeatedCompositeFieldContainer[_point3f_pb2.Point3f]
    local_scan_map: _point_cloud2_pb2.PointCloud2
    ref_corners: _containers.RepeatedCompositeFieldContainer[_point2f_pb2.Point2f]
    new_corners: _containers.RepeatedCompositeFieldContainer[_point2f_pb2.Point2f]
    corner_inliers: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., lost: bool = ..., matches: _Optional[int] = ..., inliers: _Optional[int] = ..., icp_inliers_ratio: _Optional[float] = ..., icp_rotation: _Optional[float] = ..., icp_translation: _Optional[float] = ..., icp_structural_complexity: _Optional[float] = ..., icp_structural_distribution: _Optional[float] = ..., icp_correspondences: _Optional[int] = ..., covariance: _Optional[_Iterable[float]] = ..., features: _Optional[int] = ..., local_map_size: _Optional[int] = ..., local_scan_map_size: _Optional[int] = ..., local_key_frames: _Optional[int] = ..., local_bundle_outliers: _Optional[int] = ..., local_bundle_constraints: _Optional[int] = ..., local_bundle_time: _Optional[float] = ..., key_frame_added: bool = ..., time_estimation: _Optional[float] = ..., time_particle_filtering: _Optional[float] = ..., stamp: _Optional[float] = ..., interval: _Optional[float] = ..., distance_travelled: _Optional[float] = ..., memory_usage: _Optional[int] = ..., gravity_roll_error: _Optional[float] = ..., gravity_pitch_error: _Optional[float] = ..., local_bundle_ids: _Optional[_Iterable[int]] = ..., local_bundle_models: _Optional[_Iterable[_Union[_camera_models_pb2.CameraModels, _Mapping]]] = ..., local_bundle_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., transform: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ..., transform_filtered: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ..., transform_ground_truth: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ..., guess: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ..., type: _Optional[int] = ..., words_keys: _Optional[_Iterable[int]] = ..., words_values: _Optional[_Iterable[_Union[_key_point_pb2.KeyPoint, _Mapping]]] = ..., word_matches: _Optional[_Iterable[int]] = ..., word_inliers: _Optional[_Iterable[int]] = ..., local_map_keys: _Optional[_Iterable[int]] = ..., local_map_values: _Optional[_Iterable[_Union[_point3f_pb2.Point3f, _Mapping]]] = ..., local_scan_map: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ..., ref_corners: _Optional[_Iterable[_Union[_point2f_pb2.Point2f, _Mapping]]] = ..., new_corners: _Optional[_Iterable[_Union[_point2f_pb2.Point2f, _Mapping]]] = ..., corner_inliers: _Optional[_Iterable[int]] = ...) -> None: ...
