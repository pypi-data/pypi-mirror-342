from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelSignalMask(_message.Message):
    __slots__ = ["original_mask", "gps_l1_used_in_solution", "gps_l2_used_in_solution", "gps_l3_used_in_solution", "glonass_l1_used_in_solution", "glonass_l2_used_in_solution"]
    ORIGINAL_MASK_FIELD_NUMBER: _ClassVar[int]
    GPS_L1_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    GPS_L2_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    GPS_L3_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    GLONASS_L1_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    GLONASS_L2_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    original_mask: int
    gps_l1_used_in_solution: bool
    gps_l2_used_in_solution: bool
    gps_l3_used_in_solution: bool
    glonass_l1_used_in_solution: bool
    glonass_l2_used_in_solution: bool
    def __init__(self, original_mask: _Optional[int] = ..., gps_l1_used_in_solution: bool = ..., gps_l2_used_in_solution: bool = ..., gps_l3_used_in_solution: bool = ..., glonass_l1_used_in_solution: bool = ..., glonass_l2_used_in_solution: bool = ...) -> None: ...
