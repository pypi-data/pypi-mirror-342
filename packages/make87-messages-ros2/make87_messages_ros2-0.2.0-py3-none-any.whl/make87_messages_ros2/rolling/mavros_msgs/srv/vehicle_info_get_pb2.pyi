from make87_messages_ros2.rolling.mavros_msgs.msg import vehicle_info_pb2 as _vehicle_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VehicleInfoGetRequest(_message.Message):
    __slots__ = ["sysid", "compid", "get_all"]
    SYSID_FIELD_NUMBER: _ClassVar[int]
    COMPID_FIELD_NUMBER: _ClassVar[int]
    GET_ALL_FIELD_NUMBER: _ClassVar[int]
    sysid: int
    compid: int
    get_all: bool
    def __init__(self, sysid: _Optional[int] = ..., compid: _Optional[int] = ..., get_all: bool = ...) -> None: ...

class VehicleInfoGetResponse(_message.Message):
    __slots__ = ["success", "vehicles"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    VEHICLES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    vehicles: _containers.RepeatedCompositeFieldContainer[_vehicle_info_pb2.VehicleInfo]
    def __init__(self, success: bool = ..., vehicles: _Optional[_Iterable[_Union[_vehicle_info_pb2.VehicleInfo, _Mapping]]] = ...) -> None: ...
