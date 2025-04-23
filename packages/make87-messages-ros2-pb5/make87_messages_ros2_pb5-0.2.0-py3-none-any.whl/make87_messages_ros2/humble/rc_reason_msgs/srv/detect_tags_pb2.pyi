from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import detected_tag_pb2 as _detected_tag_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import tag_pb2 as _tag_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectTagsRequest(_message.Message):
    __slots__ = ("header", "tags", "pose_frame", "robot_pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    tags: _containers.RepeatedCompositeFieldContainer[_tag_pb2.Tag]
    pose_frame: str
    robot_pose: _pose_pb2.Pose
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., tags: _Optional[_Iterable[_Union[_tag_pb2.Tag, _Mapping]]] = ..., pose_frame: _Optional[str] = ..., robot_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...

class DetectTagsResponse(_message.Message):
    __slots__ = ("header", "tags", "timestamp", "return_code")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    tags: _containers.RepeatedCompositeFieldContainer[_detected_tag_pb2.DetectedTag]
    timestamp: _time_pb2.Time
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., tags: _Optional[_Iterable[_Union[_detected_tag_pb2.DetectedTag, _Mapping]]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
