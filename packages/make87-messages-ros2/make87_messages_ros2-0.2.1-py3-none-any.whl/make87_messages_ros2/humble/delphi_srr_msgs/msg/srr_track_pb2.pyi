from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SrrTrack(_message.Message):
    __slots__ = ["header", "ros2_header", "can_tx_detect_valid_level", "can_tx_detect_status", "can_tx_detect_range_rate", "can_tx_detect_range", "can_tx_detect_angle", "can_tx_detect_amplitude"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_DETECT_VALID_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_DETECT_STATUS_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_DETECT_RANGE_RATE_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_DETECT_RANGE_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_DETECT_ANGLE_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_DETECT_AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    can_tx_detect_valid_level: int
    can_tx_detect_status: bool
    can_tx_detect_range_rate: float
    can_tx_detect_range: float
    can_tx_detect_angle: float
    can_tx_detect_amplitude: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., can_tx_detect_valid_level: _Optional[int] = ..., can_tx_detect_status: bool = ..., can_tx_detect_range_rate: _Optional[float] = ..., can_tx_detect_range: _Optional[float] = ..., can_tx_detect_angle: _Optional[float] = ..., can_tx_detect_amplitude: _Optional[float] = ...) -> None: ...
