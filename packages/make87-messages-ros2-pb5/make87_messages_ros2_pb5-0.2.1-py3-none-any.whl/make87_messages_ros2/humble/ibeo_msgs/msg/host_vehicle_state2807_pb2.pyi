from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.ibeo_msgs.msg import ibeo_data_header_pb2 as _ibeo_data_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HostVehicleState2807(_message.Message):
    __slots__ = ("header", "ros2_header", "ibeo_header", "timestamp", "distance_x", "distance_y", "course_angle", "longitudinal_velocity", "yaw_rate", "steering_wheel_angle", "cross_acceleration", "front_wheel_angle", "vehicle_width", "vehicle_front_to_front_axle", "rear_axle_to_front_axle", "rear_axle_to_vehicle_rear", "steer_ratio_poly_0", "steer_ratio_poly_1", "steer_ratio_poly_2", "steer_ratio_poly_3", "longitudinal_acceleration")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IBEO_HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_X_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_Y_FIELD_NUMBER: _ClassVar[int]
    COURSE_ANGLE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDINAL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    STEERING_WHEEL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    CROSS_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    FRONT_WHEEL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_FRONT_TO_FRONT_AXLE_FIELD_NUMBER: _ClassVar[int]
    REAR_AXLE_TO_FRONT_AXLE_FIELD_NUMBER: _ClassVar[int]
    REAR_AXLE_TO_VEHICLE_REAR_FIELD_NUMBER: _ClassVar[int]
    STEER_RATIO_POLY_0_FIELD_NUMBER: _ClassVar[int]
    STEER_RATIO_POLY_1_FIELD_NUMBER: _ClassVar[int]
    STEER_RATIO_POLY_2_FIELD_NUMBER: _ClassVar[int]
    STEER_RATIO_POLY_3_FIELD_NUMBER: _ClassVar[int]
    LONGITUDINAL_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    ibeo_header: _ibeo_data_header_pb2.IbeoDataHeader
    timestamp: _time_pb2.Time
    distance_x: int
    distance_y: int
    course_angle: float
    longitudinal_velocity: float
    yaw_rate: float
    steering_wheel_angle: float
    cross_acceleration: float
    front_wheel_angle: float
    vehicle_width: float
    vehicle_front_to_front_axle: float
    rear_axle_to_front_axle: float
    rear_axle_to_vehicle_rear: float
    steer_ratio_poly_0: float
    steer_ratio_poly_1: float
    steer_ratio_poly_2: float
    steer_ratio_poly_3: float
    longitudinal_acceleration: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., ibeo_header: _Optional[_Union[_ibeo_data_header_pb2.IbeoDataHeader, _Mapping]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., distance_x: _Optional[int] = ..., distance_y: _Optional[int] = ..., course_angle: _Optional[float] = ..., longitudinal_velocity: _Optional[float] = ..., yaw_rate: _Optional[float] = ..., steering_wheel_angle: _Optional[float] = ..., cross_acceleration: _Optional[float] = ..., front_wheel_angle: _Optional[float] = ..., vehicle_width: _Optional[float] = ..., vehicle_front_to_front_axle: _Optional[float] = ..., rear_axle_to_front_axle: _Optional[float] = ..., rear_axle_to_vehicle_rear: _Optional[float] = ..., steer_ratio_poly_0: _Optional[float] = ..., steer_ratio_poly_1: _Optional[float] = ..., steer_ratio_poly_2: _Optional[float] = ..., steer_ratio_poly_3: _Optional[float] = ..., longitudinal_acceleration: _Optional[float] = ...) -> None: ...
