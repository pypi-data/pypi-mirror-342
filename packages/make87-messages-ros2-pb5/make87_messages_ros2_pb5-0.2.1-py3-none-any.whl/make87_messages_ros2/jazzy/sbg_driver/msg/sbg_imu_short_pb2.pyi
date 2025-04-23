from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.jazzy.sbg_driver.msg import sbg_imu_status_pb2 as _sbg_imu_status_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgImuShort(_message.Message):
    __slots__ = ("header", "time_stamp", "imu_status", "delta_velocity", "delta_angle", "temperature")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    IMU_STATUS_FIELD_NUMBER: _ClassVar[int]
    DELTA_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    DELTA_ANGLE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time_stamp: int
    imu_status: _sbg_imu_status_pb2.SbgImuStatus
    delta_velocity: _vector3_pb2.Vector3
    delta_angle: _vector3_pb2.Vector3
    temperature: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., imu_status: _Optional[_Union[_sbg_imu_status_pb2.SbgImuStatus, _Mapping]] = ..., delta_velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., delta_angle: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., temperature: _Optional[int] = ...) -> None: ...
