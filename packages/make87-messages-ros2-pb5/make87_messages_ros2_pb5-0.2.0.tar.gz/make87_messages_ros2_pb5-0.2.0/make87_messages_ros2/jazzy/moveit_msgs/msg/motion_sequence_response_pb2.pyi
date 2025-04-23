from make87_messages_ros2.jazzy.moveit_msgs.msg import move_it_error_codes_pb2 as _move_it_error_codes_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import robot_trajectory_pb2 as _robot_trajectory_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MotionSequenceResponse(_message.Message):
    __slots__ = ("error_code", "sequence_start", "planned_trajectories", "planning_time")
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_START_FIELD_NUMBER: _ClassVar[int]
    PLANNED_TRAJECTORIES_FIELD_NUMBER: _ClassVar[int]
    PLANNING_TIME_FIELD_NUMBER: _ClassVar[int]
    error_code: _move_it_error_codes_pb2.MoveItErrorCodes
    sequence_start: _robot_state_pb2.RobotState
    planned_trajectories: _containers.RepeatedCompositeFieldContainer[_robot_trajectory_pb2.RobotTrajectory]
    planning_time: float
    def __init__(self, error_code: _Optional[_Union[_move_it_error_codes_pb2.MoveItErrorCodes, _Mapping]] = ..., sequence_start: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ..., planned_trajectories: _Optional[_Iterable[_Union[_robot_trajectory_pb2.RobotTrajectory, _Mapping]]] = ..., planning_time: _Optional[float] = ...) -> None: ...
