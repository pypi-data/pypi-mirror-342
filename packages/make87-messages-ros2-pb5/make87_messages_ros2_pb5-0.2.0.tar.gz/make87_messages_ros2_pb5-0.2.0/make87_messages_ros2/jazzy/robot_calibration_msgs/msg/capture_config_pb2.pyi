from make87_messages_ros2.jazzy.sensor_msgs.msg import joint_state_pb2 as _joint_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CaptureConfig(_message.Message):
    __slots__ = ("joint_states", "features")
    JOINT_STATES_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    joint_states: _joint_state_pb2.JointState
    features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, joint_states: _Optional[_Union[_joint_state_pb2.JointState, _Mapping]] = ..., features: _Optional[_Iterable[str]] = ...) -> None: ...
