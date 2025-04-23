from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MasterboardDataMsg(_message.Message):
    __slots__ = ["digital_input_bits", "digital_output_bits", "analog_input_range0", "analog_input_range1", "analog_input0", "analog_input1", "analog_output_domain0", "analog_output_domain1", "analog_output0", "analog_output1", "masterboard_temperature", "robot_voltage_48v", "robot_current", "master_io_current", "master_safety_state", "master_onoff_state"]
    DIGITAL_INPUT_BITS_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_OUTPUT_BITS_FIELD_NUMBER: _ClassVar[int]
    ANALOG_INPUT_RANGE0_FIELD_NUMBER: _ClassVar[int]
    ANALOG_INPUT_RANGE1_FIELD_NUMBER: _ClassVar[int]
    ANALOG_INPUT0_FIELD_NUMBER: _ClassVar[int]
    ANALOG_INPUT1_FIELD_NUMBER: _ClassVar[int]
    ANALOG_OUTPUT_DOMAIN0_FIELD_NUMBER: _ClassVar[int]
    ANALOG_OUTPUT_DOMAIN1_FIELD_NUMBER: _ClassVar[int]
    ANALOG_OUTPUT0_FIELD_NUMBER: _ClassVar[int]
    ANALOG_OUTPUT1_FIELD_NUMBER: _ClassVar[int]
    MASTERBOARD_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    ROBOT_VOLTAGE_48V_FIELD_NUMBER: _ClassVar[int]
    ROBOT_CURRENT_FIELD_NUMBER: _ClassVar[int]
    MASTER_IO_CURRENT_FIELD_NUMBER: _ClassVar[int]
    MASTER_SAFETY_STATE_FIELD_NUMBER: _ClassVar[int]
    MASTER_ONOFF_STATE_FIELD_NUMBER: _ClassVar[int]
    digital_input_bits: int
    digital_output_bits: int
    analog_input_range0: int
    analog_input_range1: int
    analog_input0: float
    analog_input1: float
    analog_output_domain0: int
    analog_output_domain1: int
    analog_output0: float
    analog_output1: float
    masterboard_temperature: float
    robot_voltage_48v: float
    robot_current: float
    master_io_current: float
    master_safety_state: int
    master_onoff_state: int
    def __init__(self, digital_input_bits: _Optional[int] = ..., digital_output_bits: _Optional[int] = ..., analog_input_range0: _Optional[int] = ..., analog_input_range1: _Optional[int] = ..., analog_input0: _Optional[float] = ..., analog_input1: _Optional[float] = ..., analog_output_domain0: _Optional[int] = ..., analog_output_domain1: _Optional[int] = ..., analog_output0: _Optional[float] = ..., analog_output1: _Optional[float] = ..., masterboard_temperature: _Optional[float] = ..., robot_voltage_48v: _Optional[float] = ..., robot_current: _Optional[float] = ..., master_io_current: _Optional[float] = ..., master_safety_state: _Optional[int] = ..., master_onoff_state: _Optional[int] = ...) -> None: ...
