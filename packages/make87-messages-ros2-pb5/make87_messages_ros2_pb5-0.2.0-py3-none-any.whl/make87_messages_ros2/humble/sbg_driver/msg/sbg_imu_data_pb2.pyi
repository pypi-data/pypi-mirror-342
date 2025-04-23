from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.sbg_driver.msg import sbg_imu_status_pb2 as _sbg_imu_status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgImuData(_message.Message):
    __slots__ = ("header", "ros2_header", "time_stamp", "imu_status", "accel", "gyro", "temp", "delta_vel", "delta_angle")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    IMU_STATUS_FIELD_NUMBER: _ClassVar[int]
    ACCEL_FIELD_NUMBER: _ClassVar[int]
    GYRO_FIELD_NUMBER: _ClassVar[int]
    TEMP_FIELD_NUMBER: _ClassVar[int]
    DELTA_VEL_FIELD_NUMBER: _ClassVar[int]
    DELTA_ANGLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    time_stamp: int
    imu_status: _sbg_imu_status_pb2.SbgImuStatus
    accel: _vector3_pb2.Vector3
    gyro: _vector3_pb2.Vector3
    temp: float
    delta_vel: _vector3_pb2.Vector3
    delta_angle: _vector3_pb2.Vector3
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., imu_status: _Optional[_Union[_sbg_imu_status_pb2.SbgImuStatus, _Mapping]] = ..., accel: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., gyro: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., temp: _Optional[float] = ..., delta_vel: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., delta_angle: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...
