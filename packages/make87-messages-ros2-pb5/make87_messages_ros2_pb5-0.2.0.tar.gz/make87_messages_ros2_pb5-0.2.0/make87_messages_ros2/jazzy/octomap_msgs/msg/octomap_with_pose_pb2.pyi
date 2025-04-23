from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.octomap_msgs.msg import octomap_pb2 as _octomap_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OctomapWithPose(_message.Message):
    __slots__ = ("header", "origin", "octomap")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    OCTOMAP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    origin: _pose_pb2.Pose
    octomap: _octomap_pb2.Octomap
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., origin: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., octomap: _Optional[_Union[_octomap_pb2.Octomap, _Mapping]] = ...) -> None: ...
