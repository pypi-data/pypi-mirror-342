from make87_messages_ros2.rolling.tuw_object_map_msgs.msg import geo_json_properties_pb2 as _geo_json_properties_pb2
from make87_messages_ros2.rolling.tuw_object_map_msgs.msg import geo_point_pb2 as _geo_point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeoJSONGeometry(_message.Message):
    __slots__ = ["type", "coordinates", "properties"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    type: str
    coordinates: _containers.RepeatedCompositeFieldContainer[_geo_point_pb2.GeoPoint]
    properties: _geo_json_properties_pb2.GeoJSONProperties
    def __init__(self, type: _Optional[str] = ..., coordinates: _Optional[_Iterable[_Union[_geo_point_pb2.GeoPoint, _Mapping]]] = ..., properties: _Optional[_Union[_geo_json_properties_pb2.GeoJSONProperties, _Mapping]] = ...) -> None: ...
