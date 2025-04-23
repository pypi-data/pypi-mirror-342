from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import collision_detection_pb2 as _collision_detection_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import compartment_pb2 as _compartment_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import grasp_pb2 as _grasp_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import load_carrier_pb2 as _load_carrier_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import match_pb2 as _match_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CadMatchDetectObjectRequest(_message.Message):
    __slots__ = ["header", "template_id", "pose_frame", "region_of_interest_id", "load_carrier_id", "load_carrier_compartment", "robot_pose", "collision_detection", "pose_prior_ids", "data_acquisition_mode"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    REGION_OF_INTEREST_ID_FIELD_NUMBER: _ClassVar[int]
    LOAD_CARRIER_ID_FIELD_NUMBER: _ClassVar[int]
    LOAD_CARRIER_COMPARTMENT_FIELD_NUMBER: _ClassVar[int]
    ROBOT_POSE_FIELD_NUMBER: _ClassVar[int]
    COLLISION_DETECTION_FIELD_NUMBER: _ClassVar[int]
    POSE_PRIOR_IDS_FIELD_NUMBER: _ClassVar[int]
    DATA_ACQUISITION_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    template_id: str
    pose_frame: str
    region_of_interest_id: str
    load_carrier_id: str
    load_carrier_compartment: _compartment_pb2.Compartment
    robot_pose: _pose_pb2.Pose
    collision_detection: _collision_detection_pb2.CollisionDetection
    pose_prior_ids: _containers.RepeatedScalarFieldContainer[str]
    data_acquisition_mode: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., template_id: _Optional[str] = ..., pose_frame: _Optional[str] = ..., region_of_interest_id: _Optional[str] = ..., load_carrier_id: _Optional[str] = ..., load_carrier_compartment: _Optional[_Union[_compartment_pb2.Compartment, _Mapping]] = ..., robot_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., collision_detection: _Optional[_Union[_collision_detection_pb2.CollisionDetection, _Mapping]] = ..., pose_prior_ids: _Optional[_Iterable[str]] = ..., data_acquisition_mode: _Optional[str] = ...) -> None: ...

class CadMatchDetectObjectResponse(_message.Message):
    __slots__ = ["header", "timestamp", "matches", "grasps", "load_carriers", "return_code"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    GRASPS_FIELD_NUMBER: _ClassVar[int]
    LOAD_CARRIERS_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    timestamp: _time_pb2.Time
    matches: _containers.RepeatedCompositeFieldContainer[_match_pb2.Match]
    grasps: _containers.RepeatedCompositeFieldContainer[_grasp_pb2.Grasp]
    load_carriers: _containers.RepeatedCompositeFieldContainer[_load_carrier_pb2.LoadCarrier]
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., matches: _Optional[_Iterable[_Union[_match_pb2.Match, _Mapping]]] = ..., grasps: _Optional[_Iterable[_Union[_grasp_pb2.Grasp, _Mapping]]] = ..., load_carriers: _Optional[_Iterable[_Union[_load_carrier_pb2.LoadCarrier, _Mapping]]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
