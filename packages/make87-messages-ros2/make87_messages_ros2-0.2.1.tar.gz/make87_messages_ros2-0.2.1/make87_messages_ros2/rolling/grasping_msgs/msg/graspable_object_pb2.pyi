from make87_messages_ros2.rolling.grasping_msgs.msg import object_pb2 as _object_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import grasp_pb2 as _grasp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GraspableObject(_message.Message):
    __slots__ = ["object", "grasps"]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    GRASPS_FIELD_NUMBER: _ClassVar[int]
    object: _object_pb2.Object
    grasps: _containers.RepeatedCompositeFieldContainer[_grasp_pb2.Grasp]
    def __init__(self, object: _Optional[_Union[_object_pb2.Object, _Mapping]] = ..., grasps: _Optional[_Iterable[_Union[_grasp_pb2.Grasp, _Mapping]]] = ...) -> None: ...
