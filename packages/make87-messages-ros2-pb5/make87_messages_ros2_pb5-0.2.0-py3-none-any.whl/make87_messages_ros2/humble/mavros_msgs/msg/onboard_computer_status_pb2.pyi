from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OnboardComputerStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "component", "uptime", "type", "cpu_cores", "cpu_combined", "gpu_cores", "gpu_combined", "temperature_board", "temperature_core", "fan_speed", "ram_usage", "ram_total", "storage_type", "storage_usage", "storage_total", "link_type", "link_tx_rate", "link_rx_rate", "link_tx_max", "link_rx_max")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    UPTIME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CPU_CORES_FIELD_NUMBER: _ClassVar[int]
    CPU_COMBINED_FIELD_NUMBER: _ClassVar[int]
    GPU_CORES_FIELD_NUMBER: _ClassVar[int]
    GPU_COMBINED_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_BOARD_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_CORE_FIELD_NUMBER: _ClassVar[int]
    FAN_SPEED_FIELD_NUMBER: _ClassVar[int]
    RAM_USAGE_FIELD_NUMBER: _ClassVar[int]
    RAM_TOTAL_FIELD_NUMBER: _ClassVar[int]
    STORAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_USAGE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_TOTAL_FIELD_NUMBER: _ClassVar[int]
    LINK_TYPE_FIELD_NUMBER: _ClassVar[int]
    LINK_TX_RATE_FIELD_NUMBER: _ClassVar[int]
    LINK_RX_RATE_FIELD_NUMBER: _ClassVar[int]
    LINK_TX_MAX_FIELD_NUMBER: _ClassVar[int]
    LINK_RX_MAX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    component: int
    uptime: int
    type: int
    cpu_cores: _containers.RepeatedScalarFieldContainer[int]
    cpu_combined: _containers.RepeatedScalarFieldContainer[int]
    gpu_cores: _containers.RepeatedScalarFieldContainer[int]
    gpu_combined: _containers.RepeatedScalarFieldContainer[int]
    temperature_board: int
    temperature_core: _containers.RepeatedScalarFieldContainer[int]
    fan_speed: _containers.RepeatedScalarFieldContainer[int]
    ram_usage: int
    ram_total: int
    storage_type: _containers.RepeatedScalarFieldContainer[int]
    storage_usage: _containers.RepeatedScalarFieldContainer[int]
    storage_total: _containers.RepeatedScalarFieldContainer[int]
    link_type: _containers.RepeatedScalarFieldContainer[int]
    link_tx_rate: _containers.RepeatedScalarFieldContainer[int]
    link_rx_rate: _containers.RepeatedScalarFieldContainer[int]
    link_tx_max: _containers.RepeatedScalarFieldContainer[int]
    link_rx_max: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., component: _Optional[int] = ..., uptime: _Optional[int] = ..., type: _Optional[int] = ..., cpu_cores: _Optional[_Iterable[int]] = ..., cpu_combined: _Optional[_Iterable[int]] = ..., gpu_cores: _Optional[_Iterable[int]] = ..., gpu_combined: _Optional[_Iterable[int]] = ..., temperature_board: _Optional[int] = ..., temperature_core: _Optional[_Iterable[int]] = ..., fan_speed: _Optional[_Iterable[int]] = ..., ram_usage: _Optional[int] = ..., ram_total: _Optional[int] = ..., storage_type: _Optional[_Iterable[int]] = ..., storage_usage: _Optional[_Iterable[int]] = ..., storage_total: _Optional[_Iterable[int]] = ..., link_type: _Optional[_Iterable[int]] = ..., link_tx_rate: _Optional[_Iterable[int]] = ..., link_rx_rate: _Optional[_Iterable[int]] = ..., link_tx_max: _Optional[_Iterable[int]] = ..., link_rx_max: _Optional[_Iterable[int]] = ...) -> None: ...
