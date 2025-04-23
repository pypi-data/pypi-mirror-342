from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.ros_gz_interfaces.msg import track_visual_pb2 as _track_visual_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GuiCamera(_message.Message):
    __slots__ = ("header", "name", "view_controller", "pose", "track", "projection_type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VIEW_CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    TRACK_FIELD_NUMBER: _ClassVar[int]
    PROJECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    view_controller: str
    pose: _pose_pb2.Pose
    track: _track_visual_pb2.TrackVisual
    projection_type: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., view_controller: _Optional[str] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., track: _Optional[_Union[_track_visual_pb2.TrackVisual, _Mapping]] = ..., projection_type: _Optional[str] = ...) -> None: ...
