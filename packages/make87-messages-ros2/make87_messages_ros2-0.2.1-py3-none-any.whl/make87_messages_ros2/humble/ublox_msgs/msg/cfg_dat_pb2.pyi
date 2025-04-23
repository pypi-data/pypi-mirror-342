from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgDAT(_message.Message):
    __slots__ = ["header", "datum_num", "datum_name", "maj_a", "flat", "d_x", "d_y", "d_z", "rot_x", "rot_y", "rot_z", "scale"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATUM_NUM_FIELD_NUMBER: _ClassVar[int]
    DATUM_NAME_FIELD_NUMBER: _ClassVar[int]
    MAJ_A_FIELD_NUMBER: _ClassVar[int]
    FLAT_FIELD_NUMBER: _ClassVar[int]
    D_X_FIELD_NUMBER: _ClassVar[int]
    D_Y_FIELD_NUMBER: _ClassVar[int]
    D_Z_FIELD_NUMBER: _ClassVar[int]
    ROT_X_FIELD_NUMBER: _ClassVar[int]
    ROT_Y_FIELD_NUMBER: _ClassVar[int]
    ROT_Z_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    datum_num: int
    datum_name: _containers.RepeatedScalarFieldContainer[int]
    maj_a: float
    flat: float
    d_x: float
    d_y: float
    d_z: float
    rot_x: float
    rot_y: float
    rot_z: float
    scale: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., datum_num: _Optional[int] = ..., datum_name: _Optional[_Iterable[int]] = ..., maj_a: _Optional[float] = ..., flat: _Optional[float] = ..., d_x: _Optional[float] = ..., d_y: _Optional[float] = ..., d_z: _Optional[float] = ..., rot_x: _Optional[float] = ..., rot_y: _Optional[float] = ..., rot_z: _Optional[float] = ..., scale: _Optional[float] = ...) -> None: ...
