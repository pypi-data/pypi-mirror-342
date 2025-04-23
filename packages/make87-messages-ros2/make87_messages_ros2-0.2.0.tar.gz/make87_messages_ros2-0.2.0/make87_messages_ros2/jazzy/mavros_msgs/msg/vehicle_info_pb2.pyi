from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VehicleInfo(_message.Message):
    __slots__ = ["header", "available_info", "sysid", "compid", "autopilot", "type", "system_status", "base_mode", "custom_mode", "mode", "mode_id", "capabilities", "flight_sw_version", "middleware_sw_version", "os_sw_version", "board_version", "flight_custom_version", "vendor_id", "product_id", "uid"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_INFO_FIELD_NUMBER: _ClassVar[int]
    SYSID_FIELD_NUMBER: _ClassVar[int]
    COMPID_FIELD_NUMBER: _ClassVar[int]
    AUTOPILOT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_STATUS_FIELD_NUMBER: _ClassVar[int]
    BASE_MODE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MODE_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    MODE_ID_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_SW_VERSION_FIELD_NUMBER: _ClassVar[int]
    MIDDLEWARE_SW_VERSION_FIELD_NUMBER: _ClassVar[int]
    OS_SW_VERSION_FIELD_NUMBER: _ClassVar[int]
    BOARD_VERSION_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_CUSTOM_VERSION_FIELD_NUMBER: _ClassVar[int]
    VENDOR_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    available_info: int
    sysid: int
    compid: int
    autopilot: int
    type: int
    system_status: int
    base_mode: int
    custom_mode: int
    mode: str
    mode_id: int
    capabilities: int
    flight_sw_version: int
    middleware_sw_version: int
    os_sw_version: int
    board_version: int
    flight_custom_version: str
    vendor_id: int
    product_id: int
    uid: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., available_info: _Optional[int] = ..., sysid: _Optional[int] = ..., compid: _Optional[int] = ..., autopilot: _Optional[int] = ..., type: _Optional[int] = ..., system_status: _Optional[int] = ..., base_mode: _Optional[int] = ..., custom_mode: _Optional[int] = ..., mode: _Optional[str] = ..., mode_id: _Optional[int] = ..., capabilities: _Optional[int] = ..., flight_sw_version: _Optional[int] = ..., middleware_sw_version: _Optional[int] = ..., os_sw_version: _Optional[int] = ..., board_version: _Optional[int] = ..., flight_custom_version: _Optional[str] = ..., vendor_id: _Optional[int] = ..., product_id: _Optional[int] = ..., uid: _Optional[int] = ...) -> None: ...
