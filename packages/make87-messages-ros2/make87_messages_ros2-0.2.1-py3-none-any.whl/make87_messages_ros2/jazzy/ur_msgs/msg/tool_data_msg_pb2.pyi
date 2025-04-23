from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ToolDataMsg(_message.Message):
    __slots__ = ["analog_input_range2", "analog_input_range3", "analog_input2", "analog_input3", "tool_voltage_48v", "tool_output_voltage", "tool_current", "tool_temperature", "tool_mode"]
    ANALOG_INPUT_RANGE2_FIELD_NUMBER: _ClassVar[int]
    ANALOG_INPUT_RANGE3_FIELD_NUMBER: _ClassVar[int]
    ANALOG_INPUT2_FIELD_NUMBER: _ClassVar[int]
    ANALOG_INPUT3_FIELD_NUMBER: _ClassVar[int]
    TOOL_VOLTAGE_48V_FIELD_NUMBER: _ClassVar[int]
    TOOL_OUTPUT_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    TOOL_CURRENT_FIELD_NUMBER: _ClassVar[int]
    TOOL_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOOL_MODE_FIELD_NUMBER: _ClassVar[int]
    analog_input_range2: int
    analog_input_range3: int
    analog_input2: float
    analog_input3: float
    tool_voltage_48v: float
    tool_output_voltage: int
    tool_current: float
    tool_temperature: float
    tool_mode: int
    def __init__(self, analog_input_range2: _Optional[int] = ..., analog_input_range3: _Optional[int] = ..., analog_input2: _Optional[float] = ..., analog_input3: _Optional[float] = ..., tool_voltage_48v: _Optional[float] = ..., tool_output_voltage: _Optional[int] = ..., tool_current: _Optional[float] = ..., tool_temperature: _Optional[float] = ..., tool_mode: _Optional[int] = ...) -> None: ...
