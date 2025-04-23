from make87_messages_ros2.rolling.rcss3d_agent_msgs.msg import accelerometer_pb2 as _accelerometer_pb2
from make87_messages_ros2.rolling.rcss3d_agent_msgs.msg import agent_state_pb2 as _agent_state_pb2
from make87_messages_ros2.rolling.rcss3d_agent_msgs.msg import force_resistance_pb2 as _force_resistance_pb2
from make87_messages_ros2.rolling.rcss3d_agent_msgs.msg import game_state_pb2 as _game_state_pb2
from make87_messages_ros2.rolling.rcss3d_agent_msgs.msg import gyro_rate_pb2 as _gyro_rate_pb2
from make87_messages_ros2.rolling.rcss3d_agent_msgs.msg import hear_pb2 as _hear_pb2
from make87_messages_ros2.rolling.rcss3d_agent_msgs.msg import hinge_joint_pos_pb2 as _hinge_joint_pos_pb2
from make87_messages_ros2.rolling.rcss3d_agent_msgs.msg import universal_joint_pos_pb2 as _universal_joint_pos_pb2
from make87_messages_ros2.rolling.rcss3d_agent_msgs.msg import vision_pb2 as _vision_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Percept(_message.Message):
    __slots__ = ["gyro_rates", "hinge_joints", "universal_joints", "force_resistances", "accelerometers", "vision", "game_state", "agent_state", "hears"]
    GYRO_RATES_FIELD_NUMBER: _ClassVar[int]
    HINGE_JOINTS_FIELD_NUMBER: _ClassVar[int]
    UNIVERSAL_JOINTS_FIELD_NUMBER: _ClassVar[int]
    FORCE_RESISTANCES_FIELD_NUMBER: _ClassVar[int]
    ACCELEROMETERS_FIELD_NUMBER: _ClassVar[int]
    VISION_FIELD_NUMBER: _ClassVar[int]
    GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    AGENT_STATE_FIELD_NUMBER: _ClassVar[int]
    HEARS_FIELD_NUMBER: _ClassVar[int]
    gyro_rates: _containers.RepeatedCompositeFieldContainer[_gyro_rate_pb2.GyroRate]
    hinge_joints: _containers.RepeatedCompositeFieldContainer[_hinge_joint_pos_pb2.HingeJointPos]
    universal_joints: _containers.RepeatedCompositeFieldContainer[_universal_joint_pos_pb2.UniversalJointPos]
    force_resistances: _containers.RepeatedCompositeFieldContainer[_force_resistance_pb2.ForceResistance]
    accelerometers: _containers.RepeatedCompositeFieldContainer[_accelerometer_pb2.Accelerometer]
    vision: _containers.RepeatedCompositeFieldContainer[_vision_pb2.Vision]
    game_state: _game_state_pb2.GameState
    agent_state: _containers.RepeatedCompositeFieldContainer[_agent_state_pb2.AgentState]
    hears: _containers.RepeatedCompositeFieldContainer[_hear_pb2.Hear]
    def __init__(self, gyro_rates: _Optional[_Iterable[_Union[_gyro_rate_pb2.GyroRate, _Mapping]]] = ..., hinge_joints: _Optional[_Iterable[_Union[_hinge_joint_pos_pb2.HingeJointPos, _Mapping]]] = ..., universal_joints: _Optional[_Iterable[_Union[_universal_joint_pos_pb2.UniversalJointPos, _Mapping]]] = ..., force_resistances: _Optional[_Iterable[_Union[_force_resistance_pb2.ForceResistance, _Mapping]]] = ..., accelerometers: _Optional[_Iterable[_Union[_accelerometer_pb2.Accelerometer, _Mapping]]] = ..., vision: _Optional[_Iterable[_Union[_vision_pb2.Vision, _Mapping]]] = ..., game_state: _Optional[_Union[_game_state_pb2.GameState, _Mapping]] = ..., agent_state: _Optional[_Iterable[_Union[_agent_state_pb2.AgentState, _Mapping]]] = ..., hears: _Optional[_Iterable[_Union[_hear_pb2.Hear, _Mapping]]] = ...) -> None: ...
