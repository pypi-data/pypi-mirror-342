from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MisalignmentPacket(_message.Message):
    __slots__ = ["header", "theta", "theta_variance", "phi", "phi_variance", "phi_eme", "phi_eme_variance", "status", "status_eme", "percent_negative_theta", "min_theta_sos", "max_theta_sos", "theta_sos_variance", "theta_sos_mean", "min_phi_sos", "max_phi_sos", "phi_sos_variance", "phi_sos_mean", "phi_sos_spread", "num_sos", "num_eme"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    THETA_FIELD_NUMBER: _ClassVar[int]
    THETA_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    PHI_FIELD_NUMBER: _ClassVar[int]
    PHI_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    PHI_EME_FIELD_NUMBER: _ClassVar[int]
    PHI_EME_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_EME_FIELD_NUMBER: _ClassVar[int]
    PERCENT_NEGATIVE_THETA_FIELD_NUMBER: _ClassVar[int]
    MIN_THETA_SOS_FIELD_NUMBER: _ClassVar[int]
    MAX_THETA_SOS_FIELD_NUMBER: _ClassVar[int]
    THETA_SOS_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    THETA_SOS_MEAN_FIELD_NUMBER: _ClassVar[int]
    MIN_PHI_SOS_FIELD_NUMBER: _ClassVar[int]
    MAX_PHI_SOS_FIELD_NUMBER: _ClassVar[int]
    PHI_SOS_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    PHI_SOS_MEAN_FIELD_NUMBER: _ClassVar[int]
    PHI_SOS_SPREAD_FIELD_NUMBER: _ClassVar[int]
    NUM_SOS_FIELD_NUMBER: _ClassVar[int]
    NUM_EME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    theta: float
    theta_variance: float
    phi: float
    phi_variance: float
    phi_eme: float
    phi_eme_variance: float
    status: int
    status_eme: int
    percent_negative_theta: float
    min_theta_sos: float
    max_theta_sos: float
    theta_sos_variance: float
    theta_sos_mean: float
    min_phi_sos: float
    max_phi_sos: float
    phi_sos_variance: float
    phi_sos_mean: float
    phi_sos_spread: float
    num_sos: int
    num_eme: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., theta: _Optional[float] = ..., theta_variance: _Optional[float] = ..., phi: _Optional[float] = ..., phi_variance: _Optional[float] = ..., phi_eme: _Optional[float] = ..., phi_eme_variance: _Optional[float] = ..., status: _Optional[int] = ..., status_eme: _Optional[int] = ..., percent_negative_theta: _Optional[float] = ..., min_theta_sos: _Optional[float] = ..., max_theta_sos: _Optional[float] = ..., theta_sos_variance: _Optional[float] = ..., theta_sos_mean: _Optional[float] = ..., min_phi_sos: _Optional[float] = ..., max_phi_sos: _Optional[float] = ..., phi_sos_variance: _Optional[float] = ..., phi_sos_mean: _Optional[float] = ..., phi_sos_spread: _Optional[float] = ..., num_sos: _Optional[int] = ..., num_eme: _Optional[int] = ...) -> None: ...
