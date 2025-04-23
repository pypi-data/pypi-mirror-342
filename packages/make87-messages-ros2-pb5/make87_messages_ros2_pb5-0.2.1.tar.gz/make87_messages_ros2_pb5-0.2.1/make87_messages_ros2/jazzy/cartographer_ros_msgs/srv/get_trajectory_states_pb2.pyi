from make87_messages_ros2.jazzy.cartographer_ros_msgs.msg import status_response_pb2 as _status_response_pb2
from make87_messages_ros2.jazzy.cartographer_ros_msgs.msg import trajectory_states_pb2 as _trajectory_states_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetTrajectoryStatesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTrajectoryStatesResponse(_message.Message):
    __slots__ = ("status", "trajectory_states")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_STATES_FIELD_NUMBER: _ClassVar[int]
    status: _status_response_pb2.StatusResponse
    trajectory_states: _trajectory_states_pb2.TrajectoryStates
    def __init__(self, status: _Optional[_Union[_status_response_pb2.StatusResponse, _Mapping]] = ..., trajectory_states: _Optional[_Union[_trajectory_states_pb2.TrajectoryStates, _Mapping]] = ...) -> None: ...
