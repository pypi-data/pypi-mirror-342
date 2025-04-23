from make87_messages_ros2.rolling.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.rolling.shape_msgs.msg import solid_primitive_pb2 as _solid_primitive_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegionOfInterest3D(_message.Message):
    __slots__ = ("id", "pose", "primitive")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVE_FIELD_NUMBER: _ClassVar[int]
    id: str
    pose: _pose_stamped_pb2.PoseStamped
    primitive: _solid_primitive_pb2.SolidPrimitive
    def __init__(self, id: _Optional[str] = ..., pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., primitive: _Optional[_Union[_solid_primitive_pb2.SolidPrimitive, _Mapping]] = ...) -> None: ...
