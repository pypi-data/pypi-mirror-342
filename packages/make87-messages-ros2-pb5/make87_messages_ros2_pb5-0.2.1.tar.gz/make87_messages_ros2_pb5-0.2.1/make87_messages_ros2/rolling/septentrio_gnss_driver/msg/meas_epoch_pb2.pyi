from make87_messages_ros2.rolling.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.rolling.septentrio_gnss_driver.msg import meas_epoch_channel_type1_pb2 as _meas_epoch_channel_type1_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeasEpoch(_message.Message):
    __slots__ = ("header", "block_header", "n", "sb1_length", "sb2_length", "common_flags", "cum_clk_jumps", "type1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    SB1_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SB2_LENGTH_FIELD_NUMBER: _ClassVar[int]
    COMMON_FLAGS_FIELD_NUMBER: _ClassVar[int]
    CUM_CLK_JUMPS_FIELD_NUMBER: _ClassVar[int]
    TYPE1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    n: int
    sb1_length: int
    sb2_length: int
    common_flags: int
    cum_clk_jumps: int
    type1: _containers.RepeatedCompositeFieldContainer[_meas_epoch_channel_type1_pb2.MeasEpochChannelType1]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., n: _Optional[int] = ..., sb1_length: _Optional[int] = ..., sb2_length: _Optional[int] = ..., common_flags: _Optional[int] = ..., cum_clk_jumps: _Optional[int] = ..., type1: _Optional[_Iterable[_Union[_meas_epoch_channel_type1_pb2.MeasEpochChannelType1, _Mapping]]] = ...) -> None: ...
