from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DioRealTimeData(_message.Message):
    __slots__ = ("header", "sample_frequency", "latest_sample_time", "sample_states", "sample_times")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    LATEST_SAMPLE_TIME_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_STATES_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_TIMES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sample_frequency: float
    latest_sample_time: int
    sample_states: _containers.RepeatedScalarFieldContainer[int]
    sample_times: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sample_frequency: _Optional[float] = ..., latest_sample_time: _Optional[int] = ..., sample_states: _Optional[_Iterable[int]] = ..., sample_times: _Optional[_Iterable[int]] = ...) -> None: ...
