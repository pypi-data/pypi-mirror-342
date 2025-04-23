from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import point2_df_pb2 as _point2_df_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object2280(_message.Message):
    __slots__ = ["id", "tracking_model", "mobility_of_dyn_object_detected", "motion_model_validated", "object_age", "timestamp", "object_prediction_age", "classification", "classification_certainty", "classification_age", "object_box_center", "object_box_center_sigma", "object_box_size", "object_box_orientation_angle", "object_box_orientation_angle_sigma", "relative_velocity", "relative_velocity_sigma", "absolute_velocity", "absolute_velocity_sigma", "number_of_contour_points", "closest_point_index", "reference_point_location", "reference_point_coordinate", "reference_point_coordinate_sigma", "reference_point_position_correction_coefficient", "object_priority", "object_existence_measurement", "contour_point_list"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TRACKING_MODEL_FIELD_NUMBER: _ClassVar[int]
    MOBILITY_OF_DYN_OBJECT_DETECTED_FIELD_NUMBER: _ClassVar[int]
    MOTION_MODEL_VALIDATED_FIELD_NUMBER: _ClassVar[int]
    OBJECT_AGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    OBJECT_PREDICTION_AGE_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_CERTAINTY_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_AGE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_CENTER_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_CENTER_SIGMA_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_SIZE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_ORIENTATION_ANGLE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_ORIENTATION_ANGLE_SIGMA_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_SIGMA_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_VELOCITY_SIGMA_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_CONTOUR_POINTS_FIELD_NUMBER: _ClassVar[int]
    CLOSEST_POINT_INDEX_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_LOCATION_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_COORDINATE_SIGMA_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_POSITION_CORRECTION_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    OBJECT_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    OBJECT_EXISTENCE_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    CONTOUR_POINT_LIST_FIELD_NUMBER: _ClassVar[int]
    id: int
    tracking_model: int
    mobility_of_dyn_object_detected: bool
    motion_model_validated: bool
    object_age: int
    timestamp: _time_pb2.Time
    object_prediction_age: int
    classification: int
    classification_certainty: int
    classification_age: int
    object_box_center: _point2_df_pb2.Point2Df
    object_box_center_sigma: _point2_df_pb2.Point2Df
    object_box_size: _point2_df_pb2.Point2Df
    object_box_orientation_angle: float
    object_box_orientation_angle_sigma: float
    relative_velocity: _point2_df_pb2.Point2Df
    relative_velocity_sigma: _point2_df_pb2.Point2Df
    absolute_velocity: _point2_df_pb2.Point2Df
    absolute_velocity_sigma: _point2_df_pb2.Point2Df
    number_of_contour_points: int
    closest_point_index: int
    reference_point_location: int
    reference_point_coordinate: _point2_df_pb2.Point2Df
    reference_point_coordinate_sigma: _point2_df_pb2.Point2Df
    reference_point_position_correction_coefficient: float
    object_priority: int
    object_existence_measurement: float
    contour_point_list: _containers.RepeatedCompositeFieldContainer[_point2_df_pb2.Point2Df]
    def __init__(self, id: _Optional[int] = ..., tracking_model: _Optional[int] = ..., mobility_of_dyn_object_detected: bool = ..., motion_model_validated: bool = ..., object_age: _Optional[int] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., object_prediction_age: _Optional[int] = ..., classification: _Optional[int] = ..., classification_certainty: _Optional[int] = ..., classification_age: _Optional[int] = ..., object_box_center: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., object_box_center_sigma: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., object_box_size: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., object_box_orientation_angle: _Optional[float] = ..., object_box_orientation_angle_sigma: _Optional[float] = ..., relative_velocity: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., relative_velocity_sigma: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., absolute_velocity: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., absolute_velocity_sigma: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., number_of_contour_points: _Optional[int] = ..., closest_point_index: _Optional[int] = ..., reference_point_location: _Optional[int] = ..., reference_point_coordinate: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., reference_point_coordinate_sigma: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., reference_point_position_correction_coefficient: _Optional[float] = ..., object_priority: _Optional[int] = ..., object_existence_measurement: _Optional[float] = ..., contour_point_list: _Optional[_Iterable[_Union[_point2_df_pb2.Point2Df, _Mapping]]] = ...) -> None: ...
