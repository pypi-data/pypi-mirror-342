from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RouteSegment(_message.Message):
    __slots__ = ("id", "type", "orientation", "motion_type", "start", "end", "center", "level")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    MOTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    CENTER_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    id: int
    type: int
    orientation: int
    motion_type: int
    start: _pose_pb2.Pose
    end: _pose_pb2.Pose
    center: _pose_pb2.Pose
    level: int
    def __init__(self, id: _Optional[int] = ..., type: _Optional[int] = ..., orientation: _Optional[int] = ..., motion_type: _Optional[int] = ..., start: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., end: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., center: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., level: _Optional[int] = ...) -> None: ...
