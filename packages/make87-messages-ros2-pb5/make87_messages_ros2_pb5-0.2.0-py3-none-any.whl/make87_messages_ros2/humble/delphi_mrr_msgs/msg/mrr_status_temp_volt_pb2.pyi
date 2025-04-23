from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrStatusTempVolt(_message.Message):
    __slots__ = ("header", "ros2_header", "can_batt_volts", "can_1_25_v", "can_5_v", "can_3_3_v_raw", "can_3_3_v_dac", "can_mmic_temp1", "can_processor_thermistor", "can_processor_temp1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_BATT_VOLTS_FIELD_NUMBER: _ClassVar[int]
    CAN_1_25_V_FIELD_NUMBER: _ClassVar[int]
    CAN_5_V_FIELD_NUMBER: _ClassVar[int]
    CAN_3_3_V_RAW_FIELD_NUMBER: _ClassVar[int]
    CAN_3_3_V_DAC_FIELD_NUMBER: _ClassVar[int]
    CAN_MMIC_TEMP1_FIELD_NUMBER: _ClassVar[int]
    CAN_PROCESSOR_THERMISTOR_FIELD_NUMBER: _ClassVar[int]
    CAN_PROCESSOR_TEMP1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    can_batt_volts: float
    can_1_25_v: float
    can_5_v: float
    can_3_3_v_raw: float
    can_3_3_v_dac: float
    can_mmic_temp1: int
    can_processor_thermistor: int
    can_processor_temp1: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., can_batt_volts: _Optional[float] = ..., can_1_25_v: _Optional[float] = ..., can_5_v: _Optional[float] = ..., can_3_3_v_raw: _Optional[float] = ..., can_3_3_v_dac: _Optional[float] = ..., can_mmic_temp1: _Optional[int] = ..., can_processor_thermistor: _Optional[int] = ..., can_processor_temp1: _Optional[int] = ...) -> None: ...
