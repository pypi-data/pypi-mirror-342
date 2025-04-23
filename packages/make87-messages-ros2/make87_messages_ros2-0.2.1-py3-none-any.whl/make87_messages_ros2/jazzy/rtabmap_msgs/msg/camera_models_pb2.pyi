from make87_messages_ros2.jazzy.rtabmap_msgs.msg import camera_model_pb2 as _camera_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraModels(_message.Message):
    __slots__ = ["models"]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[_camera_model_pb2.CameraModel]
    def __init__(self, models: _Optional[_Iterable[_Union[_camera_model_pb2.CameraModel, _Mapping]]] = ...) -> None: ...
