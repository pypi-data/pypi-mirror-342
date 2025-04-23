from make87_messages_ros2.rolling.marine_acoustic_msgs.msg import ping_info_pb2 as _ping_info_pb2
from make87_messages_ros2.rolling.marine_acoustic_msgs.msg import sonar_image_data_pb2 as _sonar_image_data_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RawSonarImage(_message.Message):
    __slots__ = ["header", "ping_info", "sample_rate", "samples_per_beam", "sample0", "tx_delays", "tx_angles", "rx_angles", "image"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PING_INFO_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    SAMPLES_PER_BEAM_FIELD_NUMBER: _ClassVar[int]
    SAMPLE0_FIELD_NUMBER: _ClassVar[int]
    TX_DELAYS_FIELD_NUMBER: _ClassVar[int]
    TX_ANGLES_FIELD_NUMBER: _ClassVar[int]
    RX_ANGLES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ping_info: _ping_info_pb2.PingInfo
    sample_rate: float
    samples_per_beam: int
    sample0: int
    tx_delays: _containers.RepeatedScalarFieldContainer[float]
    tx_angles: _containers.RepeatedScalarFieldContainer[float]
    rx_angles: _containers.RepeatedScalarFieldContainer[float]
    image: _sonar_image_data_pb2.SonarImageData
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ping_info: _Optional[_Union[_ping_info_pb2.PingInfo, _Mapping]] = ..., sample_rate: _Optional[float] = ..., samples_per_beam: _Optional[int] = ..., sample0: _Optional[int] = ..., tx_delays: _Optional[_Iterable[float]] = ..., tx_angles: _Optional[_Iterable[float]] = ..., rx_angles: _Optional[_Iterable[float]] = ..., image: _Optional[_Union[_sonar_image_data_pb2.SonarImageData, _Mapping]] = ...) -> None: ...
