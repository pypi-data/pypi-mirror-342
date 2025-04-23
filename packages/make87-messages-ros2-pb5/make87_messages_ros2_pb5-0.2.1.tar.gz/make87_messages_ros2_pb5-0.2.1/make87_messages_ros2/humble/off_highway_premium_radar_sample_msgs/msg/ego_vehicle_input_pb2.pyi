from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import ego_vehicle_data_pb2 as _ego_vehicle_data_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EgoVehicleInput(_message.Message):
    __slots__ = ("header", "ros2_header", "vehicle_data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    vehicle_data: _ego_vehicle_data_pb2.EgoVehicleData
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., vehicle_data: _Optional[_Union[_ego_vehicle_data_pb2.EgoVehicleData, _Mapping]] = ...) -> None: ...
