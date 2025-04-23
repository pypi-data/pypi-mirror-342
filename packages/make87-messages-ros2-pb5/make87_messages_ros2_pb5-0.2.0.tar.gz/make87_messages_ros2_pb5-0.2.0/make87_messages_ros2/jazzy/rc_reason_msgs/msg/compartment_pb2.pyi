from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import box_pb2 as _box_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Compartment(_message.Message):
    __slots__ = ("pose", "box")
    POSE_FIELD_NUMBER: _ClassVar[int]
    BOX_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_pb2.Pose
    box: _box_pb2.Box
    def __init__(self, pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., box: _Optional[_Union[_box_pb2.Box, _Mapping]] = ...) -> None: ...
