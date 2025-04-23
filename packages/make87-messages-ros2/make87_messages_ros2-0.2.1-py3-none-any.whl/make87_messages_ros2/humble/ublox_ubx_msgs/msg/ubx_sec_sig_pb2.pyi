from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import jam_state_cent_freq_pb2 as _jam_state_cent_freq_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXSecSig(_message.Message):
    __slots__ = ["header", "ros2_header", "version", "jam_det_enabled", "jamming_state", "spf_det_enabled", "spoofing_state", "jam_num_cent_freqs", "jam_state_cent_freqs"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    JAM_DET_ENABLED_FIELD_NUMBER: _ClassVar[int]
    JAMMING_STATE_FIELD_NUMBER: _ClassVar[int]
    SPF_DET_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SPOOFING_STATE_FIELD_NUMBER: _ClassVar[int]
    JAM_NUM_CENT_FREQS_FIELD_NUMBER: _ClassVar[int]
    JAM_STATE_CENT_FREQS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    version: int
    jam_det_enabled: int
    jamming_state: int
    spf_det_enabled: int
    spoofing_state: int
    jam_num_cent_freqs: int
    jam_state_cent_freqs: _containers.RepeatedCompositeFieldContainer[_jam_state_cent_freq_pb2.JamStateCentFreq]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., version: _Optional[int] = ..., jam_det_enabled: _Optional[int] = ..., jamming_state: _Optional[int] = ..., spf_det_enabled: _Optional[int] = ..., spoofing_state: _Optional[int] = ..., jam_num_cent_freqs: _Optional[int] = ..., jam_state_cent_freqs: _Optional[_Iterable[_Union[_jam_state_cent_freq_pb2.JamStateCentFreq, _Mapping]]] = ...) -> None: ...
