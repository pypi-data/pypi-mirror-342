from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.robot_calibration_msgs.msg import observation_pb2 as _observation_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import joint_state_pb2 as _joint_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CalibrationData(_message.Message):
    __slots__ = ("header", "joint_states", "observations")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    JOINT_STATES_FIELD_NUMBER: _ClassVar[int]
    OBSERVATIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    joint_states: _joint_state_pb2.JointState
    observations: _containers.RepeatedCompositeFieldContainer[_observation_pb2.Observation]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., joint_states: _Optional[_Union[_joint_state_pb2.JointState, _Mapping]] = ..., observations: _Optional[_Iterable[_Union[_observation_pb2.Observation, _Mapping]]] = ...) -> None: ...
