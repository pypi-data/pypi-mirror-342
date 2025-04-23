from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import move_it_error_codes_pb2 as _move_it_error_codes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGroupUrdfRequest(_message.Message):
    __slots__ = ("header", "group_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    group_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., group_name: _Optional[str] = ...) -> None: ...

class GetGroupUrdfResponse(_message.Message):
    __slots__ = ("header", "error_code", "urdf_string")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    URDF_STRING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    error_code: _move_it_error_codes_pb2.MoveItErrorCodes
    urdf_string: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., error_code: _Optional[_Union[_move_it_error_codes_pb2.MoveItErrorCodes, _Mapping]] = ..., urdf_string: _Optional[str] = ...) -> None: ...
