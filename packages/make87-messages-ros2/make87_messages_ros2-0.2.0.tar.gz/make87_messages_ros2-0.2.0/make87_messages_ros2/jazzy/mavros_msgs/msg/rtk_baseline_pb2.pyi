from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RTKBaseline(_message.Message):
    __slots__ = ["header", "time_last_baseline_ms", "rtk_receiver_id", "wn", "tow", "rtk_health", "rtk_rate", "nsats", "baseline_coords_type", "baseline_a_mm", "baseline_b_mm", "baseline_c_mm", "accuracy", "iar_num_hypotheses"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_LAST_BASELINE_MS_FIELD_NUMBER: _ClassVar[int]
    RTK_RECEIVER_ID_FIELD_NUMBER: _ClassVar[int]
    WN_FIELD_NUMBER: _ClassVar[int]
    TOW_FIELD_NUMBER: _ClassVar[int]
    RTK_HEALTH_FIELD_NUMBER: _ClassVar[int]
    RTK_RATE_FIELD_NUMBER: _ClassVar[int]
    NSATS_FIELD_NUMBER: _ClassVar[int]
    BASELINE_COORDS_TYPE_FIELD_NUMBER: _ClassVar[int]
    BASELINE_A_MM_FIELD_NUMBER: _ClassVar[int]
    BASELINE_B_MM_FIELD_NUMBER: _ClassVar[int]
    BASELINE_C_MM_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    IAR_NUM_HYPOTHESES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time_last_baseline_ms: int
    rtk_receiver_id: int
    wn: int
    tow: int
    rtk_health: int
    rtk_rate: int
    nsats: int
    baseline_coords_type: int
    baseline_a_mm: int
    baseline_b_mm: int
    baseline_c_mm: int
    accuracy: int
    iar_num_hypotheses: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time_last_baseline_ms: _Optional[int] = ..., rtk_receiver_id: _Optional[int] = ..., wn: _Optional[int] = ..., tow: _Optional[int] = ..., rtk_health: _Optional[int] = ..., rtk_rate: _Optional[int] = ..., nsats: _Optional[int] = ..., baseline_coords_type: _Optional[int] = ..., baseline_a_mm: _Optional[int] = ..., baseline_b_mm: _Optional[int] = ..., baseline_c_mm: _Optional[int] = ..., accuracy: _Optional[int] = ..., iar_num_hypotheses: _Optional[int] = ...) -> None: ...
