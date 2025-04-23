from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.autoware_map_msgs.msg import point_cloud_map_cell_meta_data_pb2 as _point_cloud_map_cell_meta_data_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointCloudMapCellWithID(_message.Message):
    __slots__ = ["header", "cell_id", "pointcloud", "metadata"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CELL_ID_FIELD_NUMBER: _ClassVar[int]
    POINTCLOUD_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cell_id: str
    pointcloud: _point_cloud2_pb2.PointCloud2
    metadata: _point_cloud_map_cell_meta_data_pb2.PointCloudMapCellMetaData
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cell_id: _Optional[str] = ..., pointcloud: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ..., metadata: _Optional[_Union[_point_cloud_map_cell_meta_data_pb2.PointCloudMapCellMetaData, _Mapping]] = ...) -> None: ...
