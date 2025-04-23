from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.rolling.shape_msgs.msg import plane_pb2 as _plane_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CalibrateBasePlaneRequest(_message.Message):
    __slots__ = ("pose_frame", "robot_pose", "plane_estimation_method", "stereo_plane_preference", "region_of_interest_2d_id", "offset", "plane")
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_POSE_FIELD_NUMBER: _ClassVar[int]
    PLANE_ESTIMATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    STEREO_PLANE_PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    REGION_OF_INTEREST_2D_ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    PLANE_FIELD_NUMBER: _ClassVar[int]
    pose_frame: str
    robot_pose: _pose_pb2.Pose
    plane_estimation_method: str
    stereo_plane_preference: str
    region_of_interest_2d_id: str
    offset: float
    plane: _plane_pb2.Plane
    def __init__(self, pose_frame: _Optional[str] = ..., robot_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., plane_estimation_method: _Optional[str] = ..., stereo_plane_preference: _Optional[str] = ..., region_of_interest_2d_id: _Optional[str] = ..., offset: _Optional[float] = ..., plane: _Optional[_Union[_plane_pb2.Plane, _Mapping]] = ...) -> None: ...

class CalibrateBasePlaneResponse(_message.Message):
    __slots__ = ("timestamp", "pose_frame", "plane", "return_code")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    PLANE_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _time_pb2.Time
    pose_frame: str
    plane: _plane_pb2.Plane
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., pose_frame: _Optional[str] = ..., plane: _Optional[_Union[_plane_pb2.Plane, _Mapping]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
