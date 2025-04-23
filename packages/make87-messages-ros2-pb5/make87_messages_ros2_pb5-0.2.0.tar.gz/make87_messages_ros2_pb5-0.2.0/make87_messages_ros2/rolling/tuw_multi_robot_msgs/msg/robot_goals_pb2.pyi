from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RobotGoals(_message.Message):
    __slots__ = ("robot_name", "destinations")
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    robot_name: str
    destinations: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    def __init__(self, robot_name: _Optional[str] = ..., destinations: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ...) -> None: ...
