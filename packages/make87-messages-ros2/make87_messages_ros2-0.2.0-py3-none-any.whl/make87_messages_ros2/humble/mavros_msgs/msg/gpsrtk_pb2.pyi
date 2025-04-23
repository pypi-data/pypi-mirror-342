from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GPSRTK(_message.Message):
    __slots__ = ["header", "ros2_header", "rtk_receiver_id", "wn", "tow", "rtk_health", "rtk_rate", "nsats", "baseline_a", "baseline_b", "baseline_c", "accuracy", "iar_num_hypotheses"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    RTK_RECEIVER_ID_FIELD_NUMBER: _ClassVar[int]
    WN_FIELD_NUMBER: _ClassVar[int]
    TOW_FIELD_NUMBER: _ClassVar[int]
    RTK_HEALTH_FIELD_NUMBER: _ClassVar[int]
    RTK_RATE_FIELD_NUMBER: _ClassVar[int]
    NSATS_FIELD_NUMBER: _ClassVar[int]
    BASELINE_A_FIELD_NUMBER: _ClassVar[int]
    BASELINE_B_FIELD_NUMBER: _ClassVar[int]
    BASELINE_C_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    IAR_NUM_HYPOTHESES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    rtk_receiver_id: int
    wn: int
    tow: int
    rtk_health: int
    rtk_rate: int
    nsats: int
    baseline_a: int
    baseline_b: int
    baseline_c: int
    accuracy: int
    iar_num_hypotheses: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., rtk_receiver_id: _Optional[int] = ..., wn: _Optional[int] = ..., tow: _Optional[int] = ..., rtk_health: _Optional[int] = ..., rtk_rate: _Optional[int] = ..., nsats: _Optional[int] = ..., baseline_a: _Optional[int] = ..., baseline_b: _Optional[int] = ..., baseline_c: _Optional[int] = ..., accuracy: _Optional[int] = ..., iar_num_hypotheses: _Optional[int] = ...) -> None: ...
