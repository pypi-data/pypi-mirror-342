from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CorStatusInfo(_message.Message):
    __slots__ = ["header", "protocol", "err_status", "msg_used", "correction_id", "msg_type_valid", "msg_sub_type_valid", "msg_input_handle", "msg_encrypted", "msg_decrypted"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    ERR_STATUS_FIELD_NUMBER: _ClassVar[int]
    MSG_USED_FIELD_NUMBER: _ClassVar[int]
    CORRECTION_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_VALID_FIELD_NUMBER: _ClassVar[int]
    MSG_SUB_TYPE_VALID_FIELD_NUMBER: _ClassVar[int]
    MSG_INPUT_HANDLE_FIELD_NUMBER: _ClassVar[int]
    MSG_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    MSG_DECRYPTED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    protocol: int
    err_status: int
    msg_used: int
    correction_id: int
    msg_type_valid: bool
    msg_sub_type_valid: bool
    msg_input_handle: bool
    msg_encrypted: int
    msg_decrypted: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., protocol: _Optional[int] = ..., err_status: _Optional[int] = ..., msg_used: _Optional[int] = ..., correction_id: _Optional[int] = ..., msg_type_valid: bool = ..., msg_sub_type_valid: bool = ..., msg_input_handle: bool = ..., msg_encrypted: _Optional[int] = ..., msg_decrypted: _Optional[int] = ...) -> None: ...
