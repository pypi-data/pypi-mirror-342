from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.trajectory_msgs.msg import joint_trajectory_pb2 as _joint_trajectory_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetJointTrajectoryRequest(_message.Message):
    __slots__ = ("header", "model_name", "joint_trajectory", "model_pose", "set_model_pose", "disable_physics_updates")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    JOINT_TRAJECTORY_FIELD_NUMBER: _ClassVar[int]
    MODEL_POSE_FIELD_NUMBER: _ClassVar[int]
    SET_MODEL_POSE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_PHYSICS_UPDATES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    model_name: str
    joint_trajectory: _joint_trajectory_pb2.JointTrajectory
    model_pose: _pose_pb2.Pose
    set_model_pose: bool
    disable_physics_updates: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., model_name: _Optional[str] = ..., joint_trajectory: _Optional[_Union[_joint_trajectory_pb2.JointTrajectory, _Mapping]] = ..., model_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., set_model_pose: bool = ..., disable_physics_updates: bool = ...) -> None: ...

class SetJointTrajectoryResponse(_message.Message):
    __slots__ = ("header", "success", "status_message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
