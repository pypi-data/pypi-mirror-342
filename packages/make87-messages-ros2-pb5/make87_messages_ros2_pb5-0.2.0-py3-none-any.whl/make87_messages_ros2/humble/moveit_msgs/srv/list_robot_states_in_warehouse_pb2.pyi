from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListRobotStatesInWarehouseRequest(_message.Message):
    __slots__ = ("header", "regex", "robot")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REGEX_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    regex: str
    robot: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., regex: _Optional[str] = ..., robot: _Optional[str] = ...) -> None: ...

class ListRobotStatesInWarehouseResponse(_message.Message):
    __slots__ = ("header", "states")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    states: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., states: _Optional[_Iterable[str]] = ...) -> None: ...
