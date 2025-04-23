from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RequestVoteRequest(_message.Message):
    __slots__ = ["header", "term", "candidate_id", "last_data_index", "loat_data_term"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_DATA_INDEX_FIELD_NUMBER: _ClassVar[int]
    LOAT_DATA_TERM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    term: int
    candidate_id: int
    last_data_index: int
    loat_data_term: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., term: _Optional[int] = ..., candidate_id: _Optional[int] = ..., last_data_index: _Optional[int] = ..., loat_data_term: _Optional[int] = ...) -> None: ...

class RequestVoteResponse(_message.Message):
    __slots__ = ["header", "term", "vote_granted"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    VOTE_GRANTED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    term: int
    vote_granted: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., term: _Optional[int] = ..., vote_granted: bool = ...) -> None: ...
