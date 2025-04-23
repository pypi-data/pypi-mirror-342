from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ROS2AudioMessage(_message.Message):
    __slots__ = ("header", "ros2_header", "chunk_size", "channels", "sample_rate", "encoding", "is_bigendian", "bitrate", "coding_format", "step", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CHUNK_SIZE_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    IS_BIGENDIAN_FIELD_NUMBER: _ClassVar[int]
    BITRATE_FIELD_NUMBER: _ClassVar[int]
    CODING_FORMAT_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    chunk_size: int
    channels: int
    sample_rate: int
    encoding: str
    is_bigendian: int
    bitrate: int
    coding_format: str
    step: int
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., chunk_size: _Optional[int] = ..., channels: _Optional[int] = ..., sample_rate: _Optional[int] = ..., encoding: _Optional[str] = ..., is_bigendian: _Optional[int] = ..., bitrate: _Optional[int] = ..., coding_format: _Optional[str] = ..., step: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
