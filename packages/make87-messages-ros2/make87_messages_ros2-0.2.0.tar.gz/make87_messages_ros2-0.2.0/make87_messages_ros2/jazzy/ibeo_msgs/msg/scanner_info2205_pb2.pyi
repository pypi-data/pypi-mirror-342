from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import mounting_position_f_pb2 as _mounting_position_f_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import resolution_info_pb2 as _resolution_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScannerInfo2205(_message.Message):
    __slots__ = ["device_id", "scanner_type", "scan_number", "start_angle", "end_angle", "scan_start_time", "scan_end_time", "scan_start_time_from_device", "scan_end_time_from_device", "scan_frequency", "beam_tilt", "scan_flags", "mounting_position", "resolutions"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SCANNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCAN_NUMBER_FIELD_NUMBER: _ClassVar[int]
    START_ANGLE_FIELD_NUMBER: _ClassVar[int]
    END_ANGLE_FIELD_NUMBER: _ClassVar[int]
    SCAN_START_TIME_FIELD_NUMBER: _ClassVar[int]
    SCAN_END_TIME_FIELD_NUMBER: _ClassVar[int]
    SCAN_START_TIME_FROM_DEVICE_FIELD_NUMBER: _ClassVar[int]
    SCAN_END_TIME_FROM_DEVICE_FIELD_NUMBER: _ClassVar[int]
    SCAN_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    BEAM_TILT_FIELD_NUMBER: _ClassVar[int]
    SCAN_FLAGS_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_POSITION_FIELD_NUMBER: _ClassVar[int]
    RESOLUTIONS_FIELD_NUMBER: _ClassVar[int]
    device_id: int
    scanner_type: int
    scan_number: int
    start_angle: float
    end_angle: float
    scan_start_time: _time_pb2.Time
    scan_end_time: _time_pb2.Time
    scan_start_time_from_device: _time_pb2.Time
    scan_end_time_from_device: _time_pb2.Time
    scan_frequency: float
    beam_tilt: float
    scan_flags: int
    mounting_position: _mounting_position_f_pb2.MountingPositionF
    resolutions: _containers.RepeatedCompositeFieldContainer[_resolution_info_pb2.ResolutionInfo]
    def __init__(self, device_id: _Optional[int] = ..., scanner_type: _Optional[int] = ..., scan_number: _Optional[int] = ..., start_angle: _Optional[float] = ..., end_angle: _Optional[float] = ..., scan_start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., scan_end_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., scan_start_time_from_device: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., scan_end_time_from_device: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., scan_frequency: _Optional[float] = ..., beam_tilt: _Optional[float] = ..., scan_flags: _Optional[int] = ..., mounting_position: _Optional[_Union[_mounting_position_f_pb2.MountingPositionF, _Mapping]] = ..., resolutions: _Optional[_Iterable[_Union[_resolution_info_pb2.ResolutionInfo, _Mapping]]] = ...) -> None: ...
