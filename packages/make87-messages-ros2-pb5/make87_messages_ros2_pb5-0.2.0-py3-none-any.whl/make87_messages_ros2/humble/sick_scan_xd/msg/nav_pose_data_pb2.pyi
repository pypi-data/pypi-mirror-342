from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NAVPoseData(_message.Message):
    __slots__ = ("header", "ros2_header", "x", "y", "phi", "opt_pose_data_valid", "output_mode", "timestamp", "mean_dev", "nav_mode", "info_state", "quant_used_reflectors", "pose_valid", "pose_x", "pose_y", "pose_yaw")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    PHI_FIELD_NUMBER: _ClassVar[int]
    OPT_POSE_DATA_VALID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_MODE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MEAN_DEV_FIELD_NUMBER: _ClassVar[int]
    NAV_MODE_FIELD_NUMBER: _ClassVar[int]
    INFO_STATE_FIELD_NUMBER: _ClassVar[int]
    QUANT_USED_REFLECTORS_FIELD_NUMBER: _ClassVar[int]
    POSE_VALID_FIELD_NUMBER: _ClassVar[int]
    POSE_X_FIELD_NUMBER: _ClassVar[int]
    POSE_Y_FIELD_NUMBER: _ClassVar[int]
    POSE_YAW_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    x: int
    y: int
    phi: int
    opt_pose_data_valid: int
    output_mode: int
    timestamp: int
    mean_dev: int
    nav_mode: int
    info_state: int
    quant_used_reflectors: int
    pose_valid: int
    pose_x: float
    pose_y: float
    pose_yaw: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., x: _Optional[int] = ..., y: _Optional[int] = ..., phi: _Optional[int] = ..., opt_pose_data_valid: _Optional[int] = ..., output_mode: _Optional[int] = ..., timestamp: _Optional[int] = ..., mean_dev: _Optional[int] = ..., nav_mode: _Optional[int] = ..., info_state: _Optional[int] = ..., quant_used_reflectors: _Optional[int] = ..., pose_valid: _Optional[int] = ..., pose_x: _Optional[float] = ..., pose_y: _Optional[float] = ..., pose_yaw: _Optional[float] = ...) -> None: ...
