from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrDetection(_message.Message):
    __slots__ = ["header", "detection_id", "confid_azimuth", "super_res_target", "nd_target", "host_veh_clutter", "valid_level", "azimuth", "range", "range_rate", "amplitude", "index_2lsb"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DETECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONFID_AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    SUPER_RES_TARGET_FIELD_NUMBER: _ClassVar[int]
    ND_TARGET_FIELD_NUMBER: _ClassVar[int]
    HOST_VEH_CLUTTER_FIELD_NUMBER: _ClassVar[int]
    VALID_LEVEL_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    RANGE_RATE_FIELD_NUMBER: _ClassVar[int]
    AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    INDEX_2LSB_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    detection_id: int
    confid_azimuth: int
    super_res_target: bool
    nd_target: bool
    host_veh_clutter: bool
    valid_level: bool
    azimuth: float
    range: float
    range_rate: float
    amplitude: int
    index_2lsb: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., detection_id: _Optional[int] = ..., confid_azimuth: _Optional[int] = ..., super_res_target: bool = ..., nd_target: bool = ..., host_veh_clutter: bool = ..., valid_level: bool = ..., azimuth: _Optional[float] = ..., range: _Optional[float] = ..., range_rate: _Optional[float] = ..., amplitude: _Optional[int] = ..., index_2lsb: _Optional[int] = ...) -> None: ...
