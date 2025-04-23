from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrStatus6(_message.Message):
    __slots__ = ["header", "canmsg", "supply_1p8v_a2d", "supply_n5v_a2d", "wave_diff_a2d", "sw_version_dsp_3rd_byte", "vertical_align_updated", "system_power_mode", "found_target", "recommend_unconverge", "factory_align_status_1", "factory_align_status_2", "factory_misalignment", "serv_align_updates_done", "vertical_misalignment"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    SUPPLY_1P8V_A2D_FIELD_NUMBER: _ClassVar[int]
    SUPPLY_N5V_A2D_FIELD_NUMBER: _ClassVar[int]
    WAVE_DIFF_A2D_FIELD_NUMBER: _ClassVar[int]
    SW_VERSION_DSP_3RD_BYTE_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_ALIGN_UPDATED_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_POWER_MODE_FIELD_NUMBER: _ClassVar[int]
    FOUND_TARGET_FIELD_NUMBER: _ClassVar[int]
    RECOMMEND_UNCONVERGE_FIELD_NUMBER: _ClassVar[int]
    FACTORY_ALIGN_STATUS_1_FIELD_NUMBER: _ClassVar[int]
    FACTORY_ALIGN_STATUS_2_FIELD_NUMBER: _ClassVar[int]
    FACTORY_MISALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    SERV_ALIGN_UPDATES_DONE_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_MISALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    canmsg: str
    supply_1p8v_a2d: int
    supply_n5v_a2d: int
    wave_diff_a2d: int
    sw_version_dsp_3rd_byte: int
    vertical_align_updated: bool
    system_power_mode: int
    found_target: bool
    recommend_unconverge: bool
    factory_align_status_1: int
    factory_align_status_2: int
    factory_misalignment: float
    serv_align_updates_done: int
    vertical_misalignment: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., supply_1p8v_a2d: _Optional[int] = ..., supply_n5v_a2d: _Optional[int] = ..., wave_diff_a2d: _Optional[int] = ..., sw_version_dsp_3rd_byte: _Optional[int] = ..., vertical_align_updated: bool = ..., system_power_mode: _Optional[int] = ..., found_target: bool = ..., recommend_unconverge: bool = ..., factory_align_status_1: _Optional[int] = ..., factory_align_status_2: _Optional[int] = ..., factory_misalignment: _Optional[float] = ..., serv_align_updates_done: _Optional[int] = ..., vertical_misalignment: _Optional[float] = ...) -> None: ...
