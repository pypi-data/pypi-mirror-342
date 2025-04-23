from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SbgStatusGeneral(_message.Message):
    __slots__ = ["main_power", "imu_power", "gps_power", "settings", "temperature", "datalogger", "cpu"]
    MAIN_POWER_FIELD_NUMBER: _ClassVar[int]
    IMU_POWER_FIELD_NUMBER: _ClassVar[int]
    GPS_POWER_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    DATALOGGER_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    main_power: bool
    imu_power: bool
    gps_power: bool
    settings: bool
    temperature: bool
    datalogger: bool
    cpu: bool
    def __init__(self, main_power: bool = ..., imu_power: bool = ..., gps_power: bool = ..., settings: bool = ..., temperature: bool = ..., datalogger: bool = ..., cpu: bool = ...) -> None: ...
