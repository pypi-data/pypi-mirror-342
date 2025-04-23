from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import blockade_checkpoint_pb2 as _blockade_checkpoint_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlockadeSet(_message.Message):
    __slots__ = ["participant", "reservation", "radius", "path"]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    participant: int
    reservation: int
    radius: float
    path: _containers.RepeatedCompositeFieldContainer[_blockade_checkpoint_pb2.BlockadeCheckpoint]
    def __init__(self, participant: _Optional[int] = ..., reservation: _Optional[int] = ..., radius: _Optional[float] = ..., path: _Optional[_Iterable[_Union[_blockade_checkpoint_pb2.BlockadeCheckpoint, _Mapping]]] = ...) -> None: ...
