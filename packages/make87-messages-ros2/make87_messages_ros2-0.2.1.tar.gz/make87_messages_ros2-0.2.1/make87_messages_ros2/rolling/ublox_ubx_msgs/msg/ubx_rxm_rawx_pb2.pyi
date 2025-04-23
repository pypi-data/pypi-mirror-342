from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import rawx_data_pb2 as _rawx_data_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import rec_stat_pb2 as _rec_stat_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXRxmRawx(_message.Message):
    __slots__ = ["header", "rcv_tow", "week", "leap_s", "num_meas", "rec_stat", "version", "rawx_data"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RCV_TOW_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    LEAP_S_FIELD_NUMBER: _ClassVar[int]
    NUM_MEAS_FIELD_NUMBER: _ClassVar[int]
    REC_STAT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RAWX_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    rcv_tow: float
    week: int
    leap_s: int
    num_meas: int
    rec_stat: _rec_stat_pb2.RecStat
    version: int
    rawx_data: _containers.RepeatedCompositeFieldContainer[_rawx_data_pb2.RawxData]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., rcv_tow: _Optional[float] = ..., week: _Optional[int] = ..., leap_s: _Optional[int] = ..., num_meas: _Optional[int] = ..., rec_stat: _Optional[_Union[_rec_stat_pb2.RecStat, _Mapping]] = ..., version: _Optional[int] = ..., rawx_data: _Optional[_Iterable[_Union[_rawx_data_pb2.RawxData, _Mapping]]] = ...) -> None: ...
