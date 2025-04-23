from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sick_safevisionary_interfaces.msg import roi_pb2 as _roi_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ROIArray(_message.Message):
    __slots__ = ["header", "ros2_header", "rois"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ROIS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    rois: _containers.RepeatedCompositeFieldContainer[_roi_pb2.ROI]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., rois: _Optional[_Iterable[_Union[_roi_pb2.ROI, _Mapping]]] = ...) -> None: ...
