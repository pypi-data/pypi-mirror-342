from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HilSensor(_message.Message):
    __slots__ = ("header", "ros2_header", "acc", "gyro", "mag", "abs_pressure", "diff_pressure", "pressure_alt", "temperature", "fields_updated")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ACC_FIELD_NUMBER: _ClassVar[int]
    GYRO_FIELD_NUMBER: _ClassVar[int]
    MAG_FIELD_NUMBER: _ClassVar[int]
    ABS_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    DIFF_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_ALT_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    FIELDS_UPDATED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    acc: _vector3_pb2.Vector3
    gyro: _vector3_pb2.Vector3
    mag: _vector3_pb2.Vector3
    abs_pressure: float
    diff_pressure: float
    pressure_alt: float
    temperature: float
    fields_updated: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., acc: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., gyro: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., mag: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., abs_pressure: _Optional[float] = ..., diff_pressure: _Optional[float] = ..., pressure_alt: _Optional[float] = ..., temperature: _Optional[float] = ..., fields_updated: _Optional[int] = ...) -> None: ...
