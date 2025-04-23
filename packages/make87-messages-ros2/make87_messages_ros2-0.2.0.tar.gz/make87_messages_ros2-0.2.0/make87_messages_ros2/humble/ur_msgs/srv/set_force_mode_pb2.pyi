from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_pb2 as _twist_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import wrench_pb2 as _wrench_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetForceModeRequest(_message.Message):
    __slots__ = ["header", "task_frame", "selection_vector_x", "selection_vector_y", "selection_vector_z", "selection_vector_rx", "selection_vector_ry", "selection_vector_rz", "wrench", "type", "speed_limits", "deviation_limits", "damping_factor", "gain_scaling"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TASK_FRAME_FIELD_NUMBER: _ClassVar[int]
    SELECTION_VECTOR_X_FIELD_NUMBER: _ClassVar[int]
    SELECTION_VECTOR_Y_FIELD_NUMBER: _ClassVar[int]
    SELECTION_VECTOR_Z_FIELD_NUMBER: _ClassVar[int]
    SELECTION_VECTOR_RX_FIELD_NUMBER: _ClassVar[int]
    SELECTION_VECTOR_RY_FIELD_NUMBER: _ClassVar[int]
    SELECTION_VECTOR_RZ_FIELD_NUMBER: _ClassVar[int]
    WRENCH_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SPEED_LIMITS_FIELD_NUMBER: _ClassVar[int]
    DEVIATION_LIMITS_FIELD_NUMBER: _ClassVar[int]
    DAMPING_FACTOR_FIELD_NUMBER: _ClassVar[int]
    GAIN_SCALING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    task_frame: _pose_stamped_pb2.PoseStamped
    selection_vector_x: bool
    selection_vector_y: bool
    selection_vector_z: bool
    selection_vector_rx: bool
    selection_vector_ry: bool
    selection_vector_rz: bool
    wrench: _wrench_pb2.Wrench
    type: int
    speed_limits: _twist_pb2.Twist
    deviation_limits: _containers.RepeatedScalarFieldContainer[float]
    damping_factor: float
    gain_scaling: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., task_frame: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., selection_vector_x: bool = ..., selection_vector_y: bool = ..., selection_vector_z: bool = ..., selection_vector_rx: bool = ..., selection_vector_ry: bool = ..., selection_vector_rz: bool = ..., wrench: _Optional[_Union[_wrench_pb2.Wrench, _Mapping]] = ..., type: _Optional[int] = ..., speed_limits: _Optional[_Union[_twist_pb2.Twist, _Mapping]] = ..., deviation_limits: _Optional[_Iterable[float]] = ..., damping_factor: _Optional[float] = ..., gain_scaling: _Optional[float] = ...) -> None: ...

class SetForceModeResponse(_message.Message):
    __slots__ = ["header", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
