from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import error_pb2 as _error_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import feature_info_pb2 as _feature_info_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import feature_module_pb2 as _feature_module_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FeatureInfoQueryRequest(_message.Message):
    __slots__ = ["header", "feature_names", "feature_module"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAMES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_MODULE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    feature_names: _containers.RepeatedScalarFieldContainer[str]
    feature_module: _feature_module_pb2.FeatureModule
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., feature_names: _Optional[_Iterable[str]] = ..., feature_module: _Optional[_Union[_feature_module_pb2.FeatureModule, _Mapping]] = ...) -> None: ...

class FeatureInfoQueryResponse(_message.Message):
    __slots__ = ["header", "feature_info", "error"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFO_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    feature_info: _containers.RepeatedCompositeFieldContainer[_feature_info_pb2.FeatureInfo]
    error: _error_pb2.Error
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., feature_info: _Optional[_Iterable[_Union[_feature_info_pb2.FeatureInfo, _Mapping]]] = ..., error: _Optional[_Union[_error_pb2.Error, _Mapping]] = ...) -> None: ...
