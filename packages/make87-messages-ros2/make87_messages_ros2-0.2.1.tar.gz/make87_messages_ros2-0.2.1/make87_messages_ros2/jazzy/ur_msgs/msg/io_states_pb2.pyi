from make87_messages_ros2.jazzy.ur_msgs.msg import analog_pb2 as _analog_pb2
from make87_messages_ros2.jazzy.ur_msgs.msg import digital_pb2 as _digital_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IOStates(_message.Message):
    __slots__ = ["digital_in_states", "digital_out_states", "flag_states", "analog_in_states", "analog_out_states"]
    DIGITAL_IN_STATES_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_OUT_STATES_FIELD_NUMBER: _ClassVar[int]
    FLAG_STATES_FIELD_NUMBER: _ClassVar[int]
    ANALOG_IN_STATES_FIELD_NUMBER: _ClassVar[int]
    ANALOG_OUT_STATES_FIELD_NUMBER: _ClassVar[int]
    digital_in_states: _containers.RepeatedCompositeFieldContainer[_digital_pb2.Digital]
    digital_out_states: _containers.RepeatedCompositeFieldContainer[_digital_pb2.Digital]
    flag_states: _containers.RepeatedCompositeFieldContainer[_digital_pb2.Digital]
    analog_in_states: _containers.RepeatedCompositeFieldContainer[_analog_pb2.Analog]
    analog_out_states: _containers.RepeatedCompositeFieldContainer[_analog_pb2.Analog]
    def __init__(self, digital_in_states: _Optional[_Iterable[_Union[_digital_pb2.Digital, _Mapping]]] = ..., digital_out_states: _Optional[_Iterable[_Union[_digital_pb2.Digital, _Mapping]]] = ..., flag_states: _Optional[_Iterable[_Union[_digital_pb2.Digital, _Mapping]]] = ..., analog_in_states: _Optional[_Iterable[_Union[_analog_pb2.Analog, _Mapping]]] = ..., analog_out_states: _Optional[_Iterable[_Union[_analog_pb2.Analog, _Mapping]]] = ...) -> None: ...
