from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PosCovCartesian(_message.Message):
    __slots__ = ("header", "block_header", "mode", "error", "cov_xx", "cov_yy", "cov_zz", "cov_bb", "cov_xy", "cov_xz", "cov_xb", "cov_yz", "cov_yb", "cov_zb")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COV_XX_FIELD_NUMBER: _ClassVar[int]
    COV_YY_FIELD_NUMBER: _ClassVar[int]
    COV_ZZ_FIELD_NUMBER: _ClassVar[int]
    COV_BB_FIELD_NUMBER: _ClassVar[int]
    COV_XY_FIELD_NUMBER: _ClassVar[int]
    COV_XZ_FIELD_NUMBER: _ClassVar[int]
    COV_XB_FIELD_NUMBER: _ClassVar[int]
    COV_YZ_FIELD_NUMBER: _ClassVar[int]
    COV_YB_FIELD_NUMBER: _ClassVar[int]
    COV_ZB_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    mode: int
    error: int
    cov_xx: float
    cov_yy: float
    cov_zz: float
    cov_bb: float
    cov_xy: float
    cov_xz: float
    cov_xb: float
    cov_yz: float
    cov_yb: float
    cov_zb: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., mode: _Optional[int] = ..., error: _Optional[int] = ..., cov_xx: _Optional[float] = ..., cov_yy: _Optional[float] = ..., cov_zz: _Optional[float] = ..., cov_bb: _Optional[float] = ..., cov_xy: _Optional[float] = ..., cov_xz: _Optional[float] = ..., cov_xb: _Optional[float] = ..., cov_yz: _Optional[float] = ..., cov_yb: _Optional[float] = ..., cov_zb: _Optional[float] = ...) -> None: ...
