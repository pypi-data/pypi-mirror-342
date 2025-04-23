from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import error_pb2 as _error_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import trigger_info_pb2 as _trigger_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatusRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class StatusResponse(_message.Message):
    __slots__ = ["header", "error", "display_name", "model_name", "device_firmware_version", "device_id", "device_user_id", "device_serial_number", "interface_id", "transport_layer_id", "streaming", "width", "height", "frame_rate", "pixel_format", "trigger_info", "ip_address", "mac_address"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_LAYER_ID_FIELD_NUMBER: _ClassVar[int]
    STREAMING_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
    PIXEL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_INFO_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    error: _error_pb2.Error
    display_name: str
    model_name: str
    device_firmware_version: str
    device_id: str
    device_user_id: str
    device_serial_number: str
    interface_id: str
    transport_layer_id: str
    streaming: bool
    width: int
    height: int
    frame_rate: float
    pixel_format: str
    trigger_info: _containers.RepeatedCompositeFieldContainer[_trigger_info_pb2.TriggerInfo]
    ip_address: str
    mac_address: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., error: _Optional[_Union[_error_pb2.Error, _Mapping]] = ..., display_name: _Optional[str] = ..., model_name: _Optional[str] = ..., device_firmware_version: _Optional[str] = ..., device_id: _Optional[str] = ..., device_user_id: _Optional[str] = ..., device_serial_number: _Optional[str] = ..., interface_id: _Optional[str] = ..., transport_layer_id: _Optional[str] = ..., streaming: bool = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., frame_rate: _Optional[float] = ..., pixel_format: _Optional[str] = ..., trigger_info: _Optional[_Iterable[_Union[_trigger_info_pb2.TriggerInfo, _Mapping]]] = ..., ip_address: _Optional[str] = ..., mac_address: _Optional[str] = ...) -> None: ...
