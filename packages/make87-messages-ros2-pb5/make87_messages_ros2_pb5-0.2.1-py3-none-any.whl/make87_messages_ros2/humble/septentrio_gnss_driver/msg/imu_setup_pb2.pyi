from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IMUSetup(_message.Message):
    __slots__ = ("header", "ros2_header", "block_header", "serial_port", "ant_lever_arm_x", "ant_lever_arm_y", "ant_lever_arm_z", "theta_x", "theta_y", "theta_z")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    SERIAL_PORT_FIELD_NUMBER: _ClassVar[int]
    ANT_LEVER_ARM_X_FIELD_NUMBER: _ClassVar[int]
    ANT_LEVER_ARM_Y_FIELD_NUMBER: _ClassVar[int]
    ANT_LEVER_ARM_Z_FIELD_NUMBER: _ClassVar[int]
    THETA_X_FIELD_NUMBER: _ClassVar[int]
    THETA_Y_FIELD_NUMBER: _ClassVar[int]
    THETA_Z_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    block_header: _block_header_pb2.BlockHeader
    serial_port: int
    ant_lever_arm_x: float
    ant_lever_arm_y: float
    ant_lever_arm_z: float
    theta_x: float
    theta_y: float
    theta_z: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., serial_port: _Optional[int] = ..., ant_lever_arm_x: _Optional[float] = ..., ant_lever_arm_y: _Optional[float] = ..., ant_lever_arm_z: _Optional[float] = ..., theta_x: _Optional[float] = ..., theta_y: _Optional[float] = ..., theta_z: _Optional[float] = ...) -> None: ...
