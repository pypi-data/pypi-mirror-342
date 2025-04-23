from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AudioFeatures(_message.Message):
    __slots__ = ["header", "zcr", "rms", "pitch", "hnr", "mfcc"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ZCR_FIELD_NUMBER: _ClassVar[int]
    RMS_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    HNR_FIELD_NUMBER: _ClassVar[int]
    MFCC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    zcr: float
    rms: float
    pitch: float
    hnr: float
    mfcc: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., zcr: _Optional[float] = ..., rms: _Optional[float] = ..., pitch: _Optional[float] = ..., hnr: _Optional[float] = ..., mfcc: _Optional[_Iterable[float]] = ...) -> None: ...
