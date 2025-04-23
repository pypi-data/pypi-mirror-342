from make87_messages_ros2.jazzy.kartech_linear_actuator_msgs.msg import report_index_pb2 as _report_index_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReportPollReq(_message.Message):
    __slots__ = ("header", "confirm", "report_indices")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    REPORT_INDICES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    confirm: bool
    report_indices: _containers.RepeatedCompositeFieldContainer[_report_index_pb2.ReportIndex]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., confirm: bool = ..., report_indices: _Optional[_Iterable[_Union[_report_index_pb2.ReportIndex, _Mapping]]] = ...) -> None: ...
