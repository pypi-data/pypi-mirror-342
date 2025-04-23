from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScanPoint2202(_message.Message):
    __slots__ = ["header", "layer", "echo", "transparent_point", "clutter_atmospheric", "ground", "dirt", "horizontal_angle", "radial_distance", "echo_pulse_width"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    ECHO_FIELD_NUMBER: _ClassVar[int]
    TRANSPARENT_POINT_FIELD_NUMBER: _ClassVar[int]
    CLUTTER_ATMOSPHERIC_FIELD_NUMBER: _ClassVar[int]
    GROUND_FIELD_NUMBER: _ClassVar[int]
    DIRT_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    RADIAL_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    ECHO_PULSE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    layer: int
    echo: int
    transparent_point: bool
    clutter_atmospheric: bool
    ground: bool
    dirt: bool
    horizontal_angle: int
    radial_distance: int
    echo_pulse_width: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., layer: _Optional[int] = ..., echo: _Optional[int] = ..., transparent_point: bool = ..., clutter_atmospheric: bool = ..., ground: bool = ..., dirt: bool = ..., horizontal_angle: _Optional[int] = ..., radial_distance: _Optional[int] = ..., echo_pulse_width: _Optional[int] = ...) -> None: ...
