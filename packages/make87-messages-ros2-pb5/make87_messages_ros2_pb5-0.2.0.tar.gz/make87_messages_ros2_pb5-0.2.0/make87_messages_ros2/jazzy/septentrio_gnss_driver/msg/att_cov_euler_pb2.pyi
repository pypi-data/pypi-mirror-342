from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AttCovEuler(_message.Message):
    __slots__ = ("header", "block_header", "error", "cov_headhead", "cov_pitchpitch", "cov_rollroll", "cov_headpitch", "cov_headroll", "cov_pitchroll")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COV_HEADHEAD_FIELD_NUMBER: _ClassVar[int]
    COV_PITCHPITCH_FIELD_NUMBER: _ClassVar[int]
    COV_ROLLROLL_FIELD_NUMBER: _ClassVar[int]
    COV_HEADPITCH_FIELD_NUMBER: _ClassVar[int]
    COV_HEADROLL_FIELD_NUMBER: _ClassVar[int]
    COV_PITCHROLL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    error: int
    cov_headhead: float
    cov_pitchpitch: float
    cov_rollroll: float
    cov_headpitch: float
    cov_headroll: float
    cov_pitchroll: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., error: _Optional[int] = ..., cov_headhead: _Optional[float] = ..., cov_pitchpitch: _Optional[float] = ..., cov_rollroll: _Optional[float] = ..., cov_headpitch: _Optional[float] = ..., cov_headroll: _Optional[float] = ..., cov_pitchroll: _Optional[float] = ...) -> None: ...
