from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DerivedValues(_message.Message):
    __slots__ = ["header", "multiplication_factor", "number_of_beams", "scan_time", "start_angle", "angular_beam_resolution", "interbeam_period"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MULTIPLICATION_FACTOR_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_BEAMS_FIELD_NUMBER: _ClassVar[int]
    SCAN_TIME_FIELD_NUMBER: _ClassVar[int]
    START_ANGLE_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_BEAM_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    INTERBEAM_PERIOD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    multiplication_factor: int
    number_of_beams: int
    scan_time: int
    start_angle: float
    angular_beam_resolution: float
    interbeam_period: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., multiplication_factor: _Optional[int] = ..., number_of_beams: _Optional[int] = ..., scan_time: _Optional[int] = ..., start_angle: _Optional[float] = ..., angular_beam_resolution: _Optional[float] = ..., interbeam_period: _Optional[int] = ...) -> None: ...
