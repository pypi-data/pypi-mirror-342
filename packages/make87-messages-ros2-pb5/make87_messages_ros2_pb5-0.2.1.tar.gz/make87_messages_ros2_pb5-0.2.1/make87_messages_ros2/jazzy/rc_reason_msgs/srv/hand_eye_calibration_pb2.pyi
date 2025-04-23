from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HandEyeCalibrationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HandEyeCalibrationResponse(_message.Message):
    __slots__ = ("success", "status", "message", "pose", "error", "translation_error_meter", "rotation_error_degree", "robot_mounted")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_ERROR_METER_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ERROR_DEGREE_FIELD_NUMBER: _ClassVar[int]
    ROBOT_MOUNTED_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status: int
    message: str
    pose: _pose_pb2.Pose
    error: float
    translation_error_meter: float
    rotation_error_degree: float
    robot_mounted: bool
    def __init__(self, success: bool = ..., status: _Optional[int] = ..., message: _Optional[str] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., error: _Optional[float] = ..., translation_error_meter: _Optional[float] = ..., rotation_error_degree: _Optional[float] = ..., robot_mounted: bool = ...) -> None: ...
