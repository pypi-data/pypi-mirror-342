from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PingInfo(_message.Message):
    __slots__ = ["header", "frequency", "sound_speed", "tx_beamwidths", "rx_beamwidths"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    SOUND_SPEED_FIELD_NUMBER: _ClassVar[int]
    TX_BEAMWIDTHS_FIELD_NUMBER: _ClassVar[int]
    RX_BEAMWIDTHS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    frequency: float
    sound_speed: float
    tx_beamwidths: _containers.RepeatedScalarFieldContainer[float]
    rx_beamwidths: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., frequency: _Optional[float] = ..., sound_speed: _Optional[float] = ..., tx_beamwidths: _Optional[_Iterable[float]] = ..., rx_beamwidths: _Optional[_Iterable[float]] = ...) -> None: ...
