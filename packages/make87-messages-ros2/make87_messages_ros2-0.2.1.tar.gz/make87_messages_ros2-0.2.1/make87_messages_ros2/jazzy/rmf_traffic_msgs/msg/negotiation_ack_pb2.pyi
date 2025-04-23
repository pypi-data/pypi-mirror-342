from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import negotiation_participant_ack_pb2 as _negotiation_participant_ack_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationAck(_message.Message):
    __slots__ = ["conflict_version", "acknowledgments"]
    CONFLICT_VERSION_FIELD_NUMBER: _ClassVar[int]
    ACKNOWLEDGMENTS_FIELD_NUMBER: _ClassVar[int]
    conflict_version: int
    acknowledgments: _containers.RepeatedCompositeFieldContainer[_negotiation_participant_ack_pb2.NegotiationParticipantAck]
    def __init__(self, conflict_version: _Optional[int] = ..., acknowledgments: _Optional[_Iterable[_Union[_negotiation_participant_ack_pb2.NegotiationParticipantAck, _Mapping]]] = ...) -> None: ...
