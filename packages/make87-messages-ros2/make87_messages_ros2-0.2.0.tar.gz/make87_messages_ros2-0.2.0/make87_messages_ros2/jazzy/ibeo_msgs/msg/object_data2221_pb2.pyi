from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import ibeo_data_header_pb2 as _ibeo_data_header_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import object2221_pb2 as _object2221_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectData2221(_message.Message):
    __slots__ = ["header", "ibeo_header", "scan_start_timestamp", "number_of_objects", "object_list"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IBEO_HEADER_FIELD_NUMBER: _ClassVar[int]
    SCAN_START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    OBJECT_LIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ibeo_header: _ibeo_data_header_pb2.IbeoDataHeader
    scan_start_timestamp: _time_pb2.Time
    number_of_objects: int
    object_list: _containers.RepeatedCompositeFieldContainer[_object2221_pb2.Object2221]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ibeo_header: _Optional[_Union[_ibeo_data_header_pb2.IbeoDataHeader, _Mapping]] = ..., scan_start_timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., number_of_objects: _Optional[int] = ..., object_list: _Optional[_Iterable[_Union[_object2221_pb2.Object2221, _Mapping]]] = ...) -> None: ...
