from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.cartographer_ros_msgs.msg import status_response_pb2 as _status_response_pb2
from make87_messages_ros2.humble.cartographer_ros_msgs.msg import trajectory_states_pb2 as _trajectory_states_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetTrajectoryStatesRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetTrajectoryStatesResponse(_message.Message):
    __slots__ = ["header", "status", "trajectory_states"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_STATES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: _status_response_pb2.StatusResponse
    trajectory_states: _trajectory_states_pb2.TrajectoryStates
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[_Union[_status_response_pb2.StatusResponse, _Mapping]] = ..., trajectory_states: _Optional[_Union[_trajectory_states_pb2.TrajectoryStates, _Mapping]] = ...) -> None: ...
