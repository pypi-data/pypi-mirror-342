from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RenameRobotStateInWarehouseRequest(_message.Message):
    __slots__ = ("header", "old_name", "new_name", "robot")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OLD_NAME_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    old_name: str
    new_name: str
    robot: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., old_name: _Optional[str] = ..., new_name: _Optional[str] = ..., robot: _Optional[str] = ...) -> None: ...

class RenameRobotStateInWarehouseResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
