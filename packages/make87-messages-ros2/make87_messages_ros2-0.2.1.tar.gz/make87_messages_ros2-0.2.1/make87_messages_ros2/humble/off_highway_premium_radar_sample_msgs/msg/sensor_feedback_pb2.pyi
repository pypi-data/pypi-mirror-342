from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import ego_vehicle_data_pb2 as _ego_vehicle_data_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import measurement_cycle_sync_data_pb2 as _measurement_cycle_sync_data_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorFeedback(_message.Message):
    __slots__ = ["header", "ros2_header", "lgp_version", "vehicle_time", "measurement_cycle_sync_data", "time_sync_status", "ego_vehicle_data"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LGP_VERSION_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_TIME_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENT_CYCLE_SYNC_DATA_FIELD_NUMBER: _ClassVar[int]
    TIME_SYNC_STATUS_FIELD_NUMBER: _ClassVar[int]
    EGO_VEHICLE_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    lgp_version: int
    vehicle_time: _time_pb2.Time
    measurement_cycle_sync_data: _measurement_cycle_sync_data_pb2.MeasurementCycleSyncData
    time_sync_status: int
    ego_vehicle_data: _ego_vehicle_data_pb2.EgoVehicleData
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., lgp_version: _Optional[int] = ..., vehicle_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., measurement_cycle_sync_data: _Optional[_Union[_measurement_cycle_sync_data_pb2.MeasurementCycleSyncData, _Mapping]] = ..., time_sync_status: _Optional[int] = ..., ego_vehicle_data: _Optional[_Union[_ego_vehicle_data_pb2.EgoVehicleData, _Mapping]] = ...) -> None: ...
