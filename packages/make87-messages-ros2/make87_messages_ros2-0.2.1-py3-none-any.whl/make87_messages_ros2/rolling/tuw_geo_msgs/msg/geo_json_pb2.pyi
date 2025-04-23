from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_geo_msgs.msg import geo_json_feature_pb2 as _geo_json_feature_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeoJSON(_message.Message):
    __slots__ = ["header", "type", "features"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: str
    features: _containers.RepeatedCompositeFieldContainer[_geo_json_feature_pb2.GeoJSONFeature]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[str] = ..., features: _Optional[_Iterable[_Union[_geo_json_feature_pb2.GeoJSONFeature, _Mapping]]] = ...) -> None: ...
