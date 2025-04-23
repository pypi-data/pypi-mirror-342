from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Grasp(_message.Message):
    __slots__ = ("header", "id", "uuid", "match_uuid", "pose", "priority", "gripper_id", "collision_checked")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    MATCH_UUID_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    GRIPPER_ID_FIELD_NUMBER: _ClassVar[int]
    COLLISION_CHECKED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: str
    uuid: str
    match_uuid: str
    pose: _pose_stamped_pb2.PoseStamped
    priority: int
    gripper_id: str
    collision_checked: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[str] = ..., uuid: _Optional[str] = ..., match_uuid: _Optional[str] = ..., pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., priority: _Optional[int] = ..., gripper_id: _Optional[str] = ..., collision_checked: bool = ...) -> None: ...
