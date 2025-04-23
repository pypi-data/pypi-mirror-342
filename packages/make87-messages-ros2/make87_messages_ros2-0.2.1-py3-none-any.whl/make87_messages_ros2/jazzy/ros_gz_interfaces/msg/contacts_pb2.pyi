from make87_messages_ros2.jazzy.ros_gz_interfaces.msg import contact_pb2 as _contact_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Contacts(_message.Message):
    __slots__ = ["header", "contacts"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONTACTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    contacts: _containers.RepeatedCompositeFieldContainer[_contact_pb2.Contact]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., contacts: _Optional[_Iterable[_Union[_contact_pb2.Contact, _Mapping]]] = ...) -> None: ...
