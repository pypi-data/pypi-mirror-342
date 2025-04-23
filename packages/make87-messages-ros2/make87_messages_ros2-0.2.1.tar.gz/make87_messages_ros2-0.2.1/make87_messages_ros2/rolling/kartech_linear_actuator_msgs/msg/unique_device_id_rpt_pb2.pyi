from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UniqueDeviceIdRpt(_message.Message):
    __slots__ = ["header", "actuator_id_first_6", "actuator_id_last_6"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTUATOR_ID_FIRST_6_FIELD_NUMBER: _ClassVar[int]
    ACTUATOR_ID_LAST_6_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    actuator_id_first_6: int
    actuator_id_last_6: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., actuator_id_first_6: _Optional[int] = ..., actuator_id_last_6: _Optional[int] = ...) -> None: ...
