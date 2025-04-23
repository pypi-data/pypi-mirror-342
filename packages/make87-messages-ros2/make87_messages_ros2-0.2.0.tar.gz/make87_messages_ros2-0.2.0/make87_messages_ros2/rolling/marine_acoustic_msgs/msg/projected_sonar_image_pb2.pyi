from make87_messages_ros2.rolling.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.rolling.marine_acoustic_msgs.msg import ping_info_pb2 as _ping_info_pb2
from make87_messages_ros2.rolling.marine_acoustic_msgs.msg import sonar_image_data_pb2 as _sonar_image_data_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectedSonarImage(_message.Message):
    __slots__ = ["header", "ping_info", "beam_directions", "ranges", "image"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PING_INFO_FIELD_NUMBER: _ClassVar[int]
    BEAM_DIRECTIONS_FIELD_NUMBER: _ClassVar[int]
    RANGES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ping_info: _ping_info_pb2.PingInfo
    beam_directions: _containers.RepeatedCompositeFieldContainer[_vector3_pb2.Vector3]
    ranges: _containers.RepeatedScalarFieldContainer[float]
    image: _sonar_image_data_pb2.SonarImageData
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ping_info: _Optional[_Union[_ping_info_pb2.PingInfo, _Mapping]] = ..., beam_directions: _Optional[_Iterable[_Union[_vector3_pb2.Vector3, _Mapping]]] = ..., ranges: _Optional[_Iterable[float]] = ..., image: _Optional[_Union[_sonar_image_data_pb2.SonarImageData, _Mapping]] = ...) -> None: ...
