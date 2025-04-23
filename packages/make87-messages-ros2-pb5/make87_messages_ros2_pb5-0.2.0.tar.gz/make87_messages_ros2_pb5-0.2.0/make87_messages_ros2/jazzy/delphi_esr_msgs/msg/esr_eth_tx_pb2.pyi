from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrEthTx(_message.Message):
    __slots__ = ("header", "xcp_format_version", "scan_index", "tcp_size", "xcp_scan_type", "look_index", "mmr_scan_index", "target_report_host_speed", "target_report_host_yaw_rate", "xcp_timestamp", "release_revision", "promote_revision", "field_revision", "target_report_count", "target_report_range", "target_report_range_rate", "target_report_theta", "target_report_amplitude")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    XCP_FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    SCAN_INDEX_FIELD_NUMBER: _ClassVar[int]
    TCP_SIZE_FIELD_NUMBER: _ClassVar[int]
    XCP_SCAN_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOOK_INDEX_FIELD_NUMBER: _ClassVar[int]
    MMR_SCAN_INDEX_FIELD_NUMBER: _ClassVar[int]
    TARGET_REPORT_HOST_SPEED_FIELD_NUMBER: _ClassVar[int]
    TARGET_REPORT_HOST_YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    XCP_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_REVISION_FIELD_NUMBER: _ClassVar[int]
    PROMOTE_REVISION_FIELD_NUMBER: _ClassVar[int]
    FIELD_REVISION_FIELD_NUMBER: _ClassVar[int]
    TARGET_REPORT_COUNT_FIELD_NUMBER: _ClassVar[int]
    TARGET_REPORT_RANGE_FIELD_NUMBER: _ClassVar[int]
    TARGET_REPORT_RANGE_RATE_FIELD_NUMBER: _ClassVar[int]
    TARGET_REPORT_THETA_FIELD_NUMBER: _ClassVar[int]
    TARGET_REPORT_AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    xcp_format_version: int
    scan_index: int
    tcp_size: int
    xcp_scan_type: int
    look_index: int
    mmr_scan_index: int
    target_report_host_speed: float
    target_report_host_yaw_rate: float
    xcp_timestamp: int
    release_revision: int
    promote_revision: int
    field_revision: int
    target_report_count: int
    target_report_range: _containers.RepeatedScalarFieldContainer[float]
    target_report_range_rate: _containers.RepeatedScalarFieldContainer[float]
    target_report_theta: _containers.RepeatedScalarFieldContainer[float]
    target_report_amplitude: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., xcp_format_version: _Optional[int] = ..., scan_index: _Optional[int] = ..., tcp_size: _Optional[int] = ..., xcp_scan_type: _Optional[int] = ..., look_index: _Optional[int] = ..., mmr_scan_index: _Optional[int] = ..., target_report_host_speed: _Optional[float] = ..., target_report_host_yaw_rate: _Optional[float] = ..., xcp_timestamp: _Optional[int] = ..., release_revision: _Optional[int] = ..., promote_revision: _Optional[int] = ..., field_revision: _Optional[int] = ..., target_report_count: _Optional[int] = ..., target_report_range: _Optional[_Iterable[float]] = ..., target_report_range_rate: _Optional[_Iterable[float]] = ..., target_report_theta: _Optional[_Iterable[float]] = ..., target_report_amplitude: _Optional[_Iterable[float]] = ...) -> None: ...
