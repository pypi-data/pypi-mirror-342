from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrVehicle1(_message.Message):
    __slots__ = ("header", "ros2_header", "vehicle_speed", "vehicle_speed_direction", "yaw_rate", "yaw_rate_validity", "steering_angle_rate_sign", "radius_curvature", "steering_angle_validity", "steering_angle_sign", "steering_angle", "steering_angle_rate")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_SPEED_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_SPEED_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_VALIDITY_FIELD_NUMBER: _ClassVar[int]
    STEERING_ANGLE_RATE_SIGN_FIELD_NUMBER: _ClassVar[int]
    RADIUS_CURVATURE_FIELD_NUMBER: _ClassVar[int]
    STEERING_ANGLE_VALIDITY_FIELD_NUMBER: _ClassVar[int]
    STEERING_ANGLE_SIGN_FIELD_NUMBER: _ClassVar[int]
    STEERING_ANGLE_FIELD_NUMBER: _ClassVar[int]
    STEERING_ANGLE_RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    vehicle_speed: float
    vehicle_speed_direction: bool
    yaw_rate: float
    yaw_rate_validity: bool
    steering_angle_rate_sign: bool
    radius_curvature: int
    steering_angle_validity: bool
    steering_angle_sign: bool
    steering_angle: int
    steering_angle_rate: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., vehicle_speed: _Optional[float] = ..., vehicle_speed_direction: bool = ..., yaw_rate: _Optional[float] = ..., yaw_rate_validity: bool = ..., steering_angle_rate_sign: bool = ..., radius_curvature: _Optional[int] = ..., steering_angle_validity: bool = ..., steering_angle_sign: bool = ..., steering_angle: _Optional[int] = ..., steering_angle_rate: _Optional[int] = ...) -> None: ...
