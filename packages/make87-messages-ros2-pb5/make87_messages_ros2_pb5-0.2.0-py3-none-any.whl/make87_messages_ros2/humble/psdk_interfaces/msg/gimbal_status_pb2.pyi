from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "mount_status", "is_busy", "pitch_limited", "roll_limited", "yaw_limited", "calibrating", "prev_calibration_result", "installed_direction", "disabled_mvo", "gear_show_unable", "gyro_falut", "esc_pitch_status", "esc_roll_status", "esc_yaw_status", "drone_data_recv", "init_unfinished", "fw_updating")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MOUNT_STATUS_FIELD_NUMBER: _ClassVar[int]
    IS_BUSY_FIELD_NUMBER: _ClassVar[int]
    PITCH_LIMITED_FIELD_NUMBER: _ClassVar[int]
    ROLL_LIMITED_FIELD_NUMBER: _ClassVar[int]
    YAW_LIMITED_FIELD_NUMBER: _ClassVar[int]
    CALIBRATING_FIELD_NUMBER: _ClassVar[int]
    PREV_CALIBRATION_RESULT_FIELD_NUMBER: _ClassVar[int]
    INSTALLED_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DISABLED_MVO_FIELD_NUMBER: _ClassVar[int]
    GEAR_SHOW_UNABLE_FIELD_NUMBER: _ClassVar[int]
    GYRO_FALUT_FIELD_NUMBER: _ClassVar[int]
    ESC_PITCH_STATUS_FIELD_NUMBER: _ClassVar[int]
    ESC_ROLL_STATUS_FIELD_NUMBER: _ClassVar[int]
    ESC_YAW_STATUS_FIELD_NUMBER: _ClassVar[int]
    DRONE_DATA_RECV_FIELD_NUMBER: _ClassVar[int]
    INIT_UNFINISHED_FIELD_NUMBER: _ClassVar[int]
    FW_UPDATING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    mount_status: int
    is_busy: int
    pitch_limited: int
    roll_limited: int
    yaw_limited: int
    calibrating: int
    prev_calibration_result: int
    installed_direction: int
    disabled_mvo: int
    gear_show_unable: int
    gyro_falut: int
    esc_pitch_status: int
    esc_roll_status: int
    esc_yaw_status: int
    drone_data_recv: int
    init_unfinished: int
    fw_updating: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., mount_status: _Optional[int] = ..., is_busy: _Optional[int] = ..., pitch_limited: _Optional[int] = ..., roll_limited: _Optional[int] = ..., yaw_limited: _Optional[int] = ..., calibrating: _Optional[int] = ..., prev_calibration_result: _Optional[int] = ..., installed_direction: _Optional[int] = ..., disabled_mvo: _Optional[int] = ..., gear_show_unable: _Optional[int] = ..., gyro_falut: _Optional[int] = ..., esc_pitch_status: _Optional[int] = ..., esc_roll_status: _Optional[int] = ..., esc_yaw_status: _Optional[int] = ..., drone_data_recv: _Optional[int] = ..., init_unfinished: _Optional[int] = ..., fw_updating: _Optional[int] = ...) -> None: ...
