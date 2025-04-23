from make87_messages_ros2.rolling.autoware_map_msgs.msg import area_info_pb2 as _area_info_pb2
from make87_messages_ros2.rolling.autoware_map_msgs.msg import point_cloud_map_cell_with_id_pb2 as _point_cloud_map_cell_with_id_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDifferentialPointCloudMapRequest(_message.Message):
    __slots__ = ["area", "cached_ids"]
    AREA_FIELD_NUMBER: _ClassVar[int]
    CACHED_IDS_FIELD_NUMBER: _ClassVar[int]
    area: _area_info_pb2.AreaInfo
    cached_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, area: _Optional[_Union[_area_info_pb2.AreaInfo, _Mapping]] = ..., cached_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetDifferentialPointCloudMapResponse(_message.Message):
    __slots__ = ["header", "new_pointcloud_with_ids", "ids_to_remove"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NEW_POINTCLOUD_WITH_IDS_FIELD_NUMBER: _ClassVar[int]
    IDS_TO_REMOVE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    new_pointcloud_with_ids: _containers.RepeatedCompositeFieldContainer[_point_cloud_map_cell_with_id_pb2.PointCloudMapCellWithID]
    ids_to_remove: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., new_pointcloud_with_ids: _Optional[_Iterable[_Union[_point_cloud_map_cell_with_id_pb2.PointCloudMapCellWithID, _Mapping]]] = ..., ids_to_remove: _Optional[_Iterable[str]] = ...) -> None: ...
