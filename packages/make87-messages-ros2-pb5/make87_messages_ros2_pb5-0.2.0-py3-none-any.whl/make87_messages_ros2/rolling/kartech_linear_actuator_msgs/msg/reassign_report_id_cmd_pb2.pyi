from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReassignReportIdCmd(_message.Message):
    __slots__ = ("header", "confirm", "user_report_id", "use_user_report_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    USER_REPORT_ID_FIELD_NUMBER: _ClassVar[int]
    USE_USER_REPORT_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    confirm: bool
    user_report_id: int
    use_user_report_id: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., confirm: bool = ..., user_report_id: _Optional[int] = ..., use_user_report_id: bool = ...) -> None: ...
