from make87_messages_ros2.jazzy.novatel_gps_msgs.msg import novatel_extended_solution_status_pb2 as _novatel_extended_solution_status_pb2
from make87_messages_ros2.jazzy.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.jazzy.novatel_gps_msgs.msg import novatel_signal_mask_pb2 as _novatel_signal_mask_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelDualAntennaHeading(_message.Message):
    __slots__ = ["header", "novatel_msg_header", "solution_status", "position_type", "baseline_length", "heading", "pitch", "heading_sigma", "pitch_sigma", "station_id", "num_satellites_tracked", "num_satellites_used_in_solution", "num_satellites_above_elevation_mask_angle", "num_satellites_above_elevation_mask_angle_l2", "solution_source", "extended_solution_status", "signal_mask"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    POSITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    BASELINE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    HEADING_SIGMA_FIELD_NUMBER: _ClassVar[int]
    PITCH_SIGMA_FIELD_NUMBER: _ClassVar[int]
    STATION_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_SATELLITES_TRACKED_FIELD_NUMBER: _ClassVar[int]
    NUM_SATELLITES_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    NUM_SATELLITES_ABOVE_ELEVATION_MASK_ANGLE_FIELD_NUMBER: _ClassVar[int]
    NUM_SATELLITES_ABOVE_ELEVATION_MASK_ANGLE_L2_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_SOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_MASK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    solution_status: str
    position_type: str
    baseline_length: float
    heading: float
    pitch: float
    heading_sigma: float
    pitch_sigma: float
    station_id: str
    num_satellites_tracked: int
    num_satellites_used_in_solution: int
    num_satellites_above_elevation_mask_angle: int
    num_satellites_above_elevation_mask_angle_l2: int
    solution_source: int
    extended_solution_status: _novatel_extended_solution_status_pb2.NovatelExtendedSolutionStatus
    signal_mask: _novatel_signal_mask_pb2.NovatelSignalMask
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., solution_status: _Optional[str] = ..., position_type: _Optional[str] = ..., baseline_length: _Optional[float] = ..., heading: _Optional[float] = ..., pitch: _Optional[float] = ..., heading_sigma: _Optional[float] = ..., pitch_sigma: _Optional[float] = ..., station_id: _Optional[str] = ..., num_satellites_tracked: _Optional[int] = ..., num_satellites_used_in_solution: _Optional[int] = ..., num_satellites_above_elevation_mask_angle: _Optional[int] = ..., num_satellites_above_elevation_mask_angle_l2: _Optional[int] = ..., solution_source: _Optional[int] = ..., extended_solution_status: _Optional[_Union[_novatel_extended_solution_status_pb2.NovatelExtendedSolutionStatus, _Mapping]] = ..., signal_mask: _Optional[_Union[_novatel_signal_mask_pb2.NovatelSignalMask, _Mapping]] = ...) -> None: ...
