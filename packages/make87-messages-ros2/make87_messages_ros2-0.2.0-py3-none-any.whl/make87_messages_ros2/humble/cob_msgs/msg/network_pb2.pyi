from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Network(_message.Message):
    __slots__ = ["header", "macattr", "essid", "channel", "rssi", "noise", "beacon"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MACATTR_FIELD_NUMBER: _ClassVar[int]
    ESSID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    RSSI_FIELD_NUMBER: _ClassVar[int]
    NOISE_FIELD_NUMBER: _ClassVar[int]
    BEACON_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    macattr: str
    essid: str
    channel: int
    rssi: int
    noise: int
    beacon: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., macattr: _Optional[str] = ..., essid: _Optional[str] = ..., channel: _Optional[int] = ..., rssi: _Optional[int] = ..., noise: _Optional[int] = ..., beacon: _Optional[int] = ...) -> None: ...
