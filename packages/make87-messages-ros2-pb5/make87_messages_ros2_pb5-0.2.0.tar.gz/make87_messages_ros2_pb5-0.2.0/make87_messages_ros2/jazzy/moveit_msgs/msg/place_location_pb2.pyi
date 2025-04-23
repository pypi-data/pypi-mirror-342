from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import gripper_translation_pb2 as _gripper_translation_pb2
from make87_messages_ros2.jazzy.trajectory_msgs.msg import joint_trajectory_pb2 as _joint_trajectory_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlaceLocation(_message.Message):
    __slots__ = ("id", "post_place_posture", "place_pose", "quality", "pre_place_approach", "post_place_retreat", "allowed_touch_objects")
    ID_FIELD_NUMBER: _ClassVar[int]
    POST_PLACE_POSTURE_FIELD_NUMBER: _ClassVar[int]
    PLACE_POSE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    PRE_PLACE_APPROACH_FIELD_NUMBER: _ClassVar[int]
    POST_PLACE_RETREAT_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_TOUCH_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    post_place_posture: _joint_trajectory_pb2.JointTrajectory
    place_pose: _pose_stamped_pb2.PoseStamped
    quality: float
    pre_place_approach: _gripper_translation_pb2.GripperTranslation
    post_place_retreat: _gripper_translation_pb2.GripperTranslation
    allowed_touch_objects: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., post_place_posture: _Optional[_Union[_joint_trajectory_pb2.JointTrajectory, _Mapping]] = ..., place_pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., quality: _Optional[float] = ..., pre_place_approach: _Optional[_Union[_gripper_translation_pb2.GripperTranslation, _Mapping]] = ..., post_place_retreat: _Optional[_Union[_gripper_translation_pb2.GripperTranslation, _Mapping]] = ..., allowed_touch_objects: _Optional[_Iterable[str]] = ...) -> None: ...
