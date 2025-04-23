from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Power(_message.Message):
    __slots__ = ("header", "ros2_header", "shore_power_connected", "battery_connected", "power_12v_user_nominal", "charger_connected", "charging_complete", "measured_voltages", "measured_currents")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    SHORE_POWER_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    BATTERY_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    POWER_12V_USER_NOMINAL_FIELD_NUMBER: _ClassVar[int]
    CHARGER_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    CHARGING_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    MEASURED_VOLTAGES_FIELD_NUMBER: _ClassVar[int]
    MEASURED_CURRENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    shore_power_connected: int
    battery_connected: int
    power_12v_user_nominal: int
    charger_connected: int
    charging_complete: int
    measured_voltages: _containers.RepeatedScalarFieldContainer[float]
    measured_currents: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., shore_power_connected: _Optional[int] = ..., battery_connected: _Optional[int] = ..., power_12v_user_nominal: _Optional[int] = ..., charger_connected: _Optional[int] = ..., charging_complete: _Optional[int] = ..., measured_voltages: _Optional[_Iterable[float]] = ..., measured_currents: _Optional[_Iterable[float]] = ...) -> None: ...
