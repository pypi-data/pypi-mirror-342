from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.rolling.ibeo_msgs.msg import ibeo_data_header_pb2 as _ibeo_data_header_pb2
from make87_messages_ros2.rolling.ibeo_msgs.msg import scan_point2208_pb2 as _scan_point2208_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScanData2208(_message.Message):
    __slots__ = ("header", "ibeo_header", "scan_number", "scanner_type", "motor_on", "laser_on", "frequency_locked", "motor_rotating_direction", "angle_ticks_per_rotation", "scan_flags", "mounting_yaw_angle_ticks", "mounting_pitch_angle_ticks", "mounting_roll_angle_ticks", "mounting_position_x", "mounting_position_y", "mounting_position_z", "device_id", "scan_start_time", "scan_end_time", "start_angle_ticks", "end_angle_ticks", "mirror_side", "mirror_tilt", "scan_point_list")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IBEO_HEADER_FIELD_NUMBER: _ClassVar[int]
    SCAN_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SCANNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    MOTOR_ON_FIELD_NUMBER: _ClassVar[int]
    LASER_ON_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_LOCKED_FIELD_NUMBER: _ClassVar[int]
    MOTOR_ROTATING_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    ANGLE_TICKS_PER_ROTATION_FIELD_NUMBER: _ClassVar[int]
    SCAN_FLAGS_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_YAW_ANGLE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_PITCH_ANGLE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_ROLL_ANGLE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_POSITION_Z_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SCAN_START_TIME_FIELD_NUMBER: _ClassVar[int]
    SCAN_END_TIME_FIELD_NUMBER: _ClassVar[int]
    START_ANGLE_TICKS_FIELD_NUMBER: _ClassVar[int]
    END_ANGLE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MIRROR_SIDE_FIELD_NUMBER: _ClassVar[int]
    MIRROR_TILT_FIELD_NUMBER: _ClassVar[int]
    SCAN_POINT_LIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ibeo_header: _ibeo_data_header_pb2.IbeoDataHeader
    scan_number: int
    scanner_type: int
    motor_on: bool
    laser_on: bool
    frequency_locked: bool
    motor_rotating_direction: int
    angle_ticks_per_rotation: int
    scan_flags: int
    mounting_yaw_angle_ticks: int
    mounting_pitch_angle_ticks: int
    mounting_roll_angle_ticks: int
    mounting_position_x: int
    mounting_position_y: int
    mounting_position_z: int
    device_id: int
    scan_start_time: _time_pb2.Time
    scan_end_time: _time_pb2.Time
    start_angle_ticks: int
    end_angle_ticks: int
    mirror_side: int
    mirror_tilt: int
    scan_point_list: _containers.RepeatedCompositeFieldContainer[_scan_point2208_pb2.ScanPoint2208]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ibeo_header: _Optional[_Union[_ibeo_data_header_pb2.IbeoDataHeader, _Mapping]] = ..., scan_number: _Optional[int] = ..., scanner_type: _Optional[int] = ..., motor_on: bool = ..., laser_on: bool = ..., frequency_locked: bool = ..., motor_rotating_direction: _Optional[int] = ..., angle_ticks_per_rotation: _Optional[int] = ..., scan_flags: _Optional[int] = ..., mounting_yaw_angle_ticks: _Optional[int] = ..., mounting_pitch_angle_ticks: _Optional[int] = ..., mounting_roll_angle_ticks: _Optional[int] = ..., mounting_position_x: _Optional[int] = ..., mounting_position_y: _Optional[int] = ..., mounting_position_z: _Optional[int] = ..., device_id: _Optional[int] = ..., scan_start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., scan_end_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., start_angle_ticks: _Optional[int] = ..., end_angle_ticks: _Optional[int] = ..., mirror_side: _Optional[int] = ..., mirror_tilt: _Optional[int] = ..., scan_point_list: _Optional[_Iterable[_Union[_scan_point2208_pb2.ScanPoint2208, _Mapping]]] = ...) -> None: ...
