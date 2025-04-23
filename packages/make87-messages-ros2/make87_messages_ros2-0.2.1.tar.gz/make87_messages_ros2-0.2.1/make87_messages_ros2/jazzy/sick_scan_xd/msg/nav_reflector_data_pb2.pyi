from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NAVReflectorData(_message.Message):
    __slots__ = ["cartesian_data_valid", "x", "y", "polar_data_valid", "dist", "phi", "opt_reflector_data_valid", "local_id", "global_id", "type", "sub_type", "quality", "timestamp", "size", "hit_count", "mean_echo", "start_index", "end_index", "pos_valid", "pos_x", "pos_y"]
    CARTESIAN_DATA_VALID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    POLAR_DATA_VALID_FIELD_NUMBER: _ClassVar[int]
    DIST_FIELD_NUMBER: _ClassVar[int]
    PHI_FIELD_NUMBER: _ClassVar[int]
    OPT_REFLECTOR_DATA_VALID_FIELD_NUMBER: _ClassVar[int]
    LOCAL_ID_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    HIT_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEAN_ECHO_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    END_INDEX_FIELD_NUMBER: _ClassVar[int]
    POS_VALID_FIELD_NUMBER: _ClassVar[int]
    POS_X_FIELD_NUMBER: _ClassVar[int]
    POS_Y_FIELD_NUMBER: _ClassVar[int]
    cartesian_data_valid: int
    x: int
    y: int
    polar_data_valid: int
    dist: int
    phi: int
    opt_reflector_data_valid: int
    local_id: int
    global_id: int
    type: int
    sub_type: int
    quality: int
    timestamp: int
    size: int
    hit_count: int
    mean_echo: int
    start_index: int
    end_index: int
    pos_valid: int
    pos_x: float
    pos_y: float
    def __init__(self, cartesian_data_valid: _Optional[int] = ..., x: _Optional[int] = ..., y: _Optional[int] = ..., polar_data_valid: _Optional[int] = ..., dist: _Optional[int] = ..., phi: _Optional[int] = ..., opt_reflector_data_valid: _Optional[int] = ..., local_id: _Optional[int] = ..., global_id: _Optional[int] = ..., type: _Optional[int] = ..., sub_type: _Optional[int] = ..., quality: _Optional[int] = ..., timestamp: _Optional[int] = ..., size: _Optional[int] = ..., hit_count: _Optional[int] = ..., mean_echo: _Optional[int] = ..., start_index: _Optional[int] = ..., end_index: _Optional[int] = ..., pos_valid: _Optional[int] = ..., pos_x: _Optional[float] = ..., pos_y: _Optional[float] = ...) -> None: ...
