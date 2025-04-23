from make87_messages_ros2.rolling.rmf_reservation_msgs.msg import ticket_pb2 as _ticket_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReservationAllocation(_message.Message):
    __slots__ = ["ticket", "instruction_type", "chosen_alternative", "resource"]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHOSEN_ALTERNATIVE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ticket: _ticket_pb2.Ticket
    instruction_type: int
    chosen_alternative: int
    resource: str
    def __init__(self, ticket: _Optional[_Union[_ticket_pb2.Ticket, _Mapping]] = ..., instruction_type: _Optional[int] = ..., chosen_alternative: _Optional[int] = ..., resource: _Optional[str] = ...) -> None: ...
