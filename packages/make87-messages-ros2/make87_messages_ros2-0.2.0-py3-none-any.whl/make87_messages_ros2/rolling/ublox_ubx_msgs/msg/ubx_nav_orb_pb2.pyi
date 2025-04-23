from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import orb_sv_info_pb2 as _orb_sv_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavOrb(_message.Message):
    __slots__ = ["header", "itow", "version", "num_sv", "reserved_0", "sv_info"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    RESERVED_0_FIELD_NUMBER: _ClassVar[int]
    SV_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    itow: int
    version: int
    num_sv: int
    reserved_0: _containers.RepeatedScalarFieldContainer[int]
    sv_info: _containers.RepeatedCompositeFieldContainer[_orb_sv_info_pb2.OrbSVInfo]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., itow: _Optional[int] = ..., version: _Optional[int] = ..., num_sv: _Optional[int] = ..., reserved_0: _Optional[_Iterable[int]] = ..., sv_info: _Optional[_Iterable[_Union[_orb_sv_info_pb2.OrbSVInfo, _Mapping]]] = ...) -> None: ...
