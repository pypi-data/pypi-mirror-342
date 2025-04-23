from make87_messages_ros2.rolling.marine_acoustic_msgs.msg import detection_flag_pb2 as _detection_flag_pb2
from make87_messages_ros2.rolling.marine_acoustic_msgs.msg import ping_info_pb2 as _ping_info_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SonarDetections(_message.Message):
    __slots__ = ["header", "ping_info", "flags", "two_way_travel_times", "tx_delays", "intensities", "tx_angles", "rx_angles"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PING_INFO_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    TWO_WAY_TRAVEL_TIMES_FIELD_NUMBER: _ClassVar[int]
    TX_DELAYS_FIELD_NUMBER: _ClassVar[int]
    INTENSITIES_FIELD_NUMBER: _ClassVar[int]
    TX_ANGLES_FIELD_NUMBER: _ClassVar[int]
    RX_ANGLES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ping_info: _ping_info_pb2.PingInfo
    flags: _containers.RepeatedCompositeFieldContainer[_detection_flag_pb2.DetectionFlag]
    two_way_travel_times: _containers.RepeatedScalarFieldContainer[float]
    tx_delays: _containers.RepeatedScalarFieldContainer[float]
    intensities: _containers.RepeatedScalarFieldContainer[float]
    tx_angles: _containers.RepeatedScalarFieldContainer[float]
    rx_angles: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ping_info: _Optional[_Union[_ping_info_pb2.PingInfo, _Mapping]] = ..., flags: _Optional[_Iterable[_Union[_detection_flag_pb2.DetectionFlag, _Mapping]]] = ..., two_way_travel_times: _Optional[_Iterable[float]] = ..., tx_delays: _Optional[_Iterable[float]] = ..., intensities: _Optional[_Iterable[float]] = ..., tx_angles: _Optional[_Iterable[float]] = ..., rx_angles: _Optional[_Iterable[float]] = ...) -> None: ...
