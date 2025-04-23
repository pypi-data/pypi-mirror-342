from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Dataframe(_message.Message):
    __slots__ = ("header", "ros2_header", "src_address", "dst_address", "data", "rssi")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    SRC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DST_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    RSSI_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    src_address: str
    dst_address: str
    data: _containers.RepeatedScalarFieldContainer[int]
    rssi: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., src_address: _Optional[str] = ..., dst_address: _Optional[str] = ..., data: _Optional[_Iterable[int]] = ..., rssi: _Optional[float] = ...) -> None: ...
