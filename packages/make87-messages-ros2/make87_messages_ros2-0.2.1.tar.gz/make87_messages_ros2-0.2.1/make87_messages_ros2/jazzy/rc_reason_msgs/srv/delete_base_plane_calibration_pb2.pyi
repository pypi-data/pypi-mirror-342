from make87_messages_ros2.jazzy.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteBasePlaneCalibrationRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteBasePlaneCalibrationResponse(_message.Message):
    __slots__ = ["return_code"]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
