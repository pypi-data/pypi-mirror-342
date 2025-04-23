from make87_messages_ros2.jazzy.sick_scan_xd.msg import nav_reflector_data_pb2 as _nav_reflector_data_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NAVLandmarkData(_message.Message):
    __slots__ = ["header", "landmark_filter", "num_reflectors", "reflectors"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LANDMARK_FILTER_FIELD_NUMBER: _ClassVar[int]
    NUM_REFLECTORS_FIELD_NUMBER: _ClassVar[int]
    REFLECTORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    landmark_filter: int
    num_reflectors: int
    reflectors: _containers.RepeatedCompositeFieldContainer[_nav_reflector_data_pb2.NAVReflectorData]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., landmark_filter: _Optional[int] = ..., num_reflectors: _Optional[int] = ..., reflectors: _Optional[_Iterable[_Union[_nav_reflector_data_pb2.NAVReflectorData, _Mapping]]] = ...) -> None: ...
