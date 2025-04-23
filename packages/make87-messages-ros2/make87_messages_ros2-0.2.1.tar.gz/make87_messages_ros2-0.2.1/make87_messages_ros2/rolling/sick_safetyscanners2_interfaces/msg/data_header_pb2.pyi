from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DataHeader(_message.Message):
    __slots__ = ["version_version", "version_major_version", "version_minor_version", "version_release", "serial_number_of_device", "serial_number_of_channel_plug", "channel_number", "sequence_number", "scan_number", "timestamp_date", "timestamp_time"]
    VERSION_VERSION_FIELD_NUMBER: _ClassVar[int]
    VERSION_MAJOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    VERSION_MINOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    VERSION_RELEASE_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_OF_DEVICE_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_OF_CHANNEL_PLUG_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SCAN_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_DATE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_TIME_FIELD_NUMBER: _ClassVar[int]
    version_version: int
    version_major_version: int
    version_minor_version: int
    version_release: int
    serial_number_of_device: int
    serial_number_of_channel_plug: int
    channel_number: int
    sequence_number: int
    scan_number: int
    timestamp_date: int
    timestamp_time: int
    def __init__(self, version_version: _Optional[int] = ..., version_major_version: _Optional[int] = ..., version_minor_version: _Optional[int] = ..., version_release: _Optional[int] = ..., serial_number_of_device: _Optional[int] = ..., serial_number_of_channel_plug: _Optional[int] = ..., channel_number: _Optional[int] = ..., sequence_number: _Optional[int] = ..., scan_number: _Optional[int] = ..., timestamp_date: _Optional[int] = ..., timestamp_time: _Optional[int] = ...) -> None: ...
