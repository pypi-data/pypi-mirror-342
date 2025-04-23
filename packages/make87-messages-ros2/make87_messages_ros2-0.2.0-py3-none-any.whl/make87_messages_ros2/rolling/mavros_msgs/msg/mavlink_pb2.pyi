from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Mavlink(_message.Message):
    __slots__ = ["header", "framing_status", "magic", "len", "incompat_flags", "compat_flags", "seq", "sysid", "compid", "msgid", "checksum", "payload64", "signature"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FRAMING_STATUS_FIELD_NUMBER: _ClassVar[int]
    MAGIC_FIELD_NUMBER: _ClassVar[int]
    LEN_FIELD_NUMBER: _ClassVar[int]
    INCOMPAT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    COMPAT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    SYSID_FIELD_NUMBER: _ClassVar[int]
    COMPID_FIELD_NUMBER: _ClassVar[int]
    MSGID_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD64_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    framing_status: int
    magic: int
    len: int
    incompat_flags: int
    compat_flags: int
    seq: int
    sysid: int
    compid: int
    msgid: int
    checksum: int
    payload64: _containers.RepeatedScalarFieldContainer[int]
    signature: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., framing_status: _Optional[int] = ..., magic: _Optional[int] = ..., len: _Optional[int] = ..., incompat_flags: _Optional[int] = ..., compat_flags: _Optional[int] = ..., seq: _Optional[int] = ..., sysid: _Optional[int] = ..., compid: _Optional[int] = ..., msgid: _Optional[int] = ..., checksum: _Optional[int] = ..., payload64: _Optional[_Iterable[int]] = ..., signature: _Optional[_Iterable[int]] = ...) -> None: ...
