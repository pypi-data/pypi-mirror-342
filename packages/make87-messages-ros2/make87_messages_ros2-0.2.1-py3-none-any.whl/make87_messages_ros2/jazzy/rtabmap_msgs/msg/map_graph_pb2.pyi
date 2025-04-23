from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import transform_pb2 as _transform_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import link_pb2 as _link_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapGraph(_message.Message):
    __slots__ = ["header", "map_to_odom", "poses_id", "poses", "links"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_TO_ODOM_FIELD_NUMBER: _ClassVar[int]
    POSES_ID_FIELD_NUMBER: _ClassVar[int]
    POSES_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map_to_odom: _transform_pb2.Transform
    poses_id: _containers.RepeatedScalarFieldContainer[int]
    poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    links: _containers.RepeatedCompositeFieldContainer[_link_pb2.Link]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map_to_odom: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ..., poses_id: _Optional[_Iterable[int]] = ..., poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., links: _Optional[_Iterable[_Union[_link_pb2.Link, _Mapping]]] = ...) -> None: ...
