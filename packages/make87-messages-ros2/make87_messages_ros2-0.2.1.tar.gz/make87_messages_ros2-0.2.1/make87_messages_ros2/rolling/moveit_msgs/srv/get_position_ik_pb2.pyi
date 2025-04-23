from make87_messages_ros2.rolling.moveit_msgs.msg import move_it_error_codes_pb2 as _move_it_error_codes_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import position_ik_request_pb2 as _position_ik_request_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPositionIKRequest(_message.Message):
    __slots__ = ["ik_request"]
    IK_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ik_request: _position_ik_request_pb2.PositionIKRequest
    def __init__(self, ik_request: _Optional[_Union[_position_ik_request_pb2.PositionIKRequest, _Mapping]] = ...) -> None: ...

class GetPositionIKResponse(_message.Message):
    __slots__ = ["solution", "error_code"]
    SOLUTION_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    solution: _robot_state_pb2.RobotState
    error_code: _move_it_error_codes_pb2.MoveItErrorCodes
    def __init__(self, solution: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ..., error_code: _Optional[_Union[_move_it_error_codes_pb2.MoveItErrorCodes, _Mapping]] = ...) -> None: ...
