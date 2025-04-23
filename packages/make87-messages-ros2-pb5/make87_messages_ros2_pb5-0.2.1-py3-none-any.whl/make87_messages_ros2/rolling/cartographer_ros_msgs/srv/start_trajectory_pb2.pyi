from make87_messages_ros2.rolling.cartographer_ros_msgs.msg import status_response_pb2 as _status_response_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartTrajectoryRequest(_message.Message):
    __slots__ = ("configuration_directory", "configuration_basename", "use_initial_pose", "initial_pose", "relative_to_trajectory_id")
    CONFIGURATION_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_BASENAME_FIELD_NUMBER: _ClassVar[int]
    USE_INITIAL_POSE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_POSE_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_TO_TRAJECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    configuration_directory: str
    configuration_basename: str
    use_initial_pose: bool
    initial_pose: _pose_pb2.Pose
    relative_to_trajectory_id: int
    def __init__(self, configuration_directory: _Optional[str] = ..., configuration_basename: _Optional[str] = ..., use_initial_pose: bool = ..., initial_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., relative_to_trajectory_id: _Optional[int] = ...) -> None: ...

class StartTrajectoryResponse(_message.Message):
    __slots__ = ("status", "trajectory_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    status: _status_response_pb2.StatusResponse
    trajectory_id: int
    def __init__(self, status: _Optional[_Union[_status_response_pb2.StatusResponse, _Mapping]] = ..., trajectory_id: _Optional[int] = ...) -> None: ...
