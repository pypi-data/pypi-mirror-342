from make87_messages_ros2.jazzy.geographic_msgs.msg import geo_pose_pb2 as _geo_pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetDatumRequest(_message.Message):
    __slots__ = ["geo_pose"]
    GEO_POSE_FIELD_NUMBER: _ClassVar[int]
    geo_pose: _geo_pose_pb2.GeoPose
    def __init__(self, geo_pose: _Optional[_Union[_geo_pose_pb2.GeoPose, _Mapping]] = ...) -> None: ...

class SetDatumResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
