from make87_messages_ros2.jazzy.geometry_msgs.msg import wrench_pb2 as _wrench_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import string_pb2 as _string_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import u_int32_pb2 as _u_int32_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JointWrench(_message.Message):
    __slots__ = ("header", "body_1_name", "body_1_id", "body_2_name", "body_2_id", "body_1_wrench", "body_2_wrench")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_1_NAME_FIELD_NUMBER: _ClassVar[int]
    BODY_1_ID_FIELD_NUMBER: _ClassVar[int]
    BODY_2_NAME_FIELD_NUMBER: _ClassVar[int]
    BODY_2_ID_FIELD_NUMBER: _ClassVar[int]
    BODY_1_WRENCH_FIELD_NUMBER: _ClassVar[int]
    BODY_2_WRENCH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    body_1_name: _string_pb2.String
    body_1_id: _u_int32_pb2.UInt32
    body_2_name: _string_pb2.String
    body_2_id: _u_int32_pb2.UInt32
    body_1_wrench: _wrench_pb2.Wrench
    body_2_wrench: _wrench_pb2.Wrench
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., body_1_name: _Optional[_Union[_string_pb2.String, _Mapping]] = ..., body_1_id: _Optional[_Union[_u_int32_pb2.UInt32, _Mapping]] = ..., body_2_name: _Optional[_Union[_string_pb2.String, _Mapping]] = ..., body_2_id: _Optional[_Union[_u_int32_pb2.UInt32, _Mapping]] = ..., body_1_wrench: _Optional[_Union[_wrench_pb2.Wrench, _Mapping]] = ..., body_2_wrench: _Optional[_Union[_wrench_pb2.Wrench, _Mapping]] = ...) -> None: ...
