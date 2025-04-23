from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import region_of_interest2_d_pb2 as _region_of_interest2_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetRegionOfInterest2DRequest(_message.Message):
    __slots__ = ["header", "region_of_interest_2d"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REGION_OF_INTEREST_2D_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    region_of_interest_2d: _region_of_interest2_d_pb2.RegionOfInterest2D
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., region_of_interest_2d: _Optional[_Union[_region_of_interest2_d_pb2.RegionOfInterest2D, _Mapping]] = ...) -> None: ...

class SetRegionOfInterest2DResponse(_message.Message):
    __slots__ = ["header", "return_code"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
