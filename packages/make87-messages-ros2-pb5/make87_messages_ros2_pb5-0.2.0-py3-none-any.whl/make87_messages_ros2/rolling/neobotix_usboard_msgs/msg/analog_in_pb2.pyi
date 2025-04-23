from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnalogIn(_message.Message):
    __slots__ = ("header", "command", "analog_data_ch4_low_byte", "analog_data_ch4_high_bits", "analog_data_ch3_low_byte", "analog_data_ch3_high_bits", "analog_data_ch2_low_byte", "analog_data_ch2_high_bits", "analog_data_ch1_low_byte", "analog_data_ch1_high_bits")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    ANALOG_DATA_CH4_LOW_BYTE_FIELD_NUMBER: _ClassVar[int]
    ANALOG_DATA_CH4_HIGH_BITS_FIELD_NUMBER: _ClassVar[int]
    ANALOG_DATA_CH3_LOW_BYTE_FIELD_NUMBER: _ClassVar[int]
    ANALOG_DATA_CH3_HIGH_BITS_FIELD_NUMBER: _ClassVar[int]
    ANALOG_DATA_CH2_LOW_BYTE_FIELD_NUMBER: _ClassVar[int]
    ANALOG_DATA_CH2_HIGH_BITS_FIELD_NUMBER: _ClassVar[int]
    ANALOG_DATA_CH1_LOW_BYTE_FIELD_NUMBER: _ClassVar[int]
    ANALOG_DATA_CH1_HIGH_BITS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    command: int
    analog_data_ch4_low_byte: int
    analog_data_ch4_high_bits: int
    analog_data_ch3_low_byte: int
    analog_data_ch3_high_bits: int
    analog_data_ch2_low_byte: int
    analog_data_ch2_high_bits: int
    analog_data_ch1_low_byte: int
    analog_data_ch1_high_bits: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., command: _Optional[int] = ..., analog_data_ch4_low_byte: _Optional[int] = ..., analog_data_ch4_high_bits: _Optional[int] = ..., analog_data_ch3_low_byte: _Optional[int] = ..., analog_data_ch3_high_bits: _Optional[int] = ..., analog_data_ch2_low_byte: _Optional[int] = ..., analog_data_ch2_high_bits: _Optional[int] = ..., analog_data_ch1_low_byte: _Optional[int] = ..., analog_data_ch1_high_bits: _Optional[int] = ...) -> None: ...
