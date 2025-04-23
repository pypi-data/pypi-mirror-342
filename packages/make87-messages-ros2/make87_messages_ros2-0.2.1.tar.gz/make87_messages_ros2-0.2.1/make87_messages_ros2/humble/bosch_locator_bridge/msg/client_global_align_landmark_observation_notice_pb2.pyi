from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientGlobalAlignLandmarkObservationNotice(_message.Message):
    __slots__ = ["header", "pose_index", "landmark_index"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_INDEX_FIELD_NUMBER: _ClassVar[int]
    LANDMARK_INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pose_index: int
    landmark_index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pose_index: _Optional[int] = ..., landmark_index: _Optional[int] = ...) -> None: ...
