from make87_messages_ros2.rolling.marker_msgs.msg import marker_with_covariance_pb2 as _marker_with_covariance_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkerWithCovarianceStamped(_message.Message):
    __slots__ = ("header", "marker")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MARKER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    marker: _marker_with_covariance_pb2.MarkerWithCovariance
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., marker: _Optional[_Union[_marker_with_covariance_pb2.MarkerWithCovariance, _Mapping]] = ...) -> None: ...
