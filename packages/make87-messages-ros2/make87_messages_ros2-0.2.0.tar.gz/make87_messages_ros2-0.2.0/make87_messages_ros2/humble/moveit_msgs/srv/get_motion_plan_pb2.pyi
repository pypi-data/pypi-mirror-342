from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import motion_plan_request_pb2 as _motion_plan_request_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import motion_plan_response_pb2 as _motion_plan_response_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetMotionPlanRequest(_message.Message):
    __slots__ = ["header", "motion_plan_request"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MOTION_PLAN_REQUEST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    motion_plan_request: _motion_plan_request_pb2.MotionPlanRequest
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., motion_plan_request: _Optional[_Union[_motion_plan_request_pb2.MotionPlanRequest, _Mapping]] = ...) -> None: ...

class GetMotionPlanResponse(_message.Message):
    __slots__ = ["header", "motion_plan_response"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MOTION_PLAN_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    motion_plan_response: _motion_plan_response_pb2.MotionPlanResponse
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., motion_plan_response: _Optional[_Union[_motion_plan_response_pb2.MotionPlanResponse, _Mapping]] = ...) -> None: ...
