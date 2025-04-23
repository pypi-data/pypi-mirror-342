from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import grid_size_pb2 as _grid_size_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import load_carrier_with_filling_level_pb2 as _load_carrier_with_filling_level_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectFillingLevelRequest(_message.Message):
    __slots__ = ["pose_frame", "region_of_interest_id", "region_of_interest_2d_id", "load_carrier_ids", "robot_pose", "filling_level_cell_count"]
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    REGION_OF_INTEREST_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_OF_INTEREST_2D_ID_FIELD_NUMBER: _ClassVar[int]
    LOAD_CARRIER_IDS_FIELD_NUMBER: _ClassVar[int]
    ROBOT_POSE_FIELD_NUMBER: _ClassVar[int]
    FILLING_LEVEL_CELL_COUNT_FIELD_NUMBER: _ClassVar[int]
    pose_frame: str
    region_of_interest_id: str
    region_of_interest_2d_id: str
    load_carrier_ids: _containers.RepeatedScalarFieldContainer[str]
    robot_pose: _pose_pb2.Pose
    filling_level_cell_count: _grid_size_pb2.GridSize
    def __init__(self, pose_frame: _Optional[str] = ..., region_of_interest_id: _Optional[str] = ..., region_of_interest_2d_id: _Optional[str] = ..., load_carrier_ids: _Optional[_Iterable[str]] = ..., robot_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., filling_level_cell_count: _Optional[_Union[_grid_size_pb2.GridSize, _Mapping]] = ...) -> None: ...

class DetectFillingLevelResponse(_message.Message):
    __slots__ = ["timestamp", "load_carriers", "return_code"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LOAD_CARRIERS_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _time_pb2.Time
    load_carriers: _containers.RepeatedCompositeFieldContainer[_load_carrier_with_filling_level_pb2.LoadCarrierWithFillingLevel]
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., load_carriers: _Optional[_Iterable[_Union[_load_carrier_with_filling_level_pb2.LoadCarrierWithFillingLevel, _Mapping]]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
