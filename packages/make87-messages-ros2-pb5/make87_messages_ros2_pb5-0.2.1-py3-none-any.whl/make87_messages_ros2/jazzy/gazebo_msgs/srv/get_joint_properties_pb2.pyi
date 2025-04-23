from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetJointPropertiesRequest(_message.Message):
    __slots__ = ("joint_name",)
    JOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    joint_name: str
    def __init__(self, joint_name: _Optional[str] = ...) -> None: ...

class GetJointPropertiesResponse(_message.Message):
    __slots__ = ("type", "damping", "position", "rate", "success", "status_message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DAMPING_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: int
    damping: _containers.RepeatedScalarFieldContainer[float]
    position: _containers.RepeatedScalarFieldContainer[float]
    rate: _containers.RepeatedScalarFieldContainer[float]
    success: bool
    status_message: str
    def __init__(self, type: _Optional[int] = ..., damping: _Optional[_Iterable[float]] = ..., position: _Optional[_Iterable[float]] = ..., rate: _Optional[_Iterable[float]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
