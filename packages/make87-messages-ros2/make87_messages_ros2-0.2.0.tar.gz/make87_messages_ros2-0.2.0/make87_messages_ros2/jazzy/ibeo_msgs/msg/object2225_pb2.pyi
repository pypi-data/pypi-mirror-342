from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import point2_df_pb2 as _point2_df_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object2225(_message.Message):
    __slots__ = ["id", "age", "timestamp", "hidden_status_age", "classification", "classification_certainty", "classification_age", "bounding_box_center", "bounding_box_size", "object_box_center", "object_box_center_sigma", "object_box_size", "yaw_angle", "relative_velocity", "relative_velocity_sigma", "absolute_velocity", "absolute_velocity_sigma", "number_of_contour_points", "closest_point_index", "contour_point_list"]
    ID_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_STATUS_AGE_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_CERTAINTY_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_AGE_FIELD_NUMBER: _ClassVar[int]
    BOUNDING_BOX_CENTER_FIELD_NUMBER: _ClassVar[int]
    BOUNDING_BOX_SIZE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_CENTER_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_CENTER_SIGMA_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_SIZE_FIELD_NUMBER: _ClassVar[int]
    YAW_ANGLE_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_SIGMA_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_VELOCITY_SIGMA_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_CONTOUR_POINTS_FIELD_NUMBER: _ClassVar[int]
    CLOSEST_POINT_INDEX_FIELD_NUMBER: _ClassVar[int]
    CONTOUR_POINT_LIST_FIELD_NUMBER: _ClassVar[int]
    id: int
    age: int
    timestamp: _time_pb2.Time
    hidden_status_age: int
    classification: int
    classification_certainty: int
    classification_age: int
    bounding_box_center: _point2_df_pb2.Point2Df
    bounding_box_size: _point2_df_pb2.Point2Df
    object_box_center: _point2_df_pb2.Point2Df
    object_box_center_sigma: _point2_df_pb2.Point2Df
    object_box_size: _point2_df_pb2.Point2Df
    yaw_angle: float
    relative_velocity: _point2_df_pb2.Point2Df
    relative_velocity_sigma: _point2_df_pb2.Point2Df
    absolute_velocity: _point2_df_pb2.Point2Df
    absolute_velocity_sigma: _point2_df_pb2.Point2Df
    number_of_contour_points: int
    closest_point_index: int
    contour_point_list: _containers.RepeatedCompositeFieldContainer[_point2_df_pb2.Point2Df]
    def __init__(self, id: _Optional[int] = ..., age: _Optional[int] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., hidden_status_age: _Optional[int] = ..., classification: _Optional[int] = ..., classification_certainty: _Optional[int] = ..., classification_age: _Optional[int] = ..., bounding_box_center: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., bounding_box_size: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., object_box_center: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., object_box_center_sigma: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., object_box_size: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., yaw_angle: _Optional[float] = ..., relative_velocity: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., relative_velocity_sigma: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., absolute_velocity: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., absolute_velocity_sigma: _Optional[_Union[_point2_df_pb2.Point2Df, _Mapping]] = ..., number_of_contour_points: _Optional[int] = ..., closest_point_index: _Optional[int] = ..., contour_point_list: _Optional[_Iterable[_Union[_point2_df_pb2.Point2Df, _Mapping]]] = ...) -> None: ...
