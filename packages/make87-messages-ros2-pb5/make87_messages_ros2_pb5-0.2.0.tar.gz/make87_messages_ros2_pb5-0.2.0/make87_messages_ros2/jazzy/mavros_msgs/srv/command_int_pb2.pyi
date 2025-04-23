from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CommandIntRequest(_message.Message):
    __slots__ = ("broadcast", "frame", "command", "current", "autocontinue", "param1", "param2", "param3", "param4", "x", "y", "z")
    BROADCAST_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    AUTOCONTINUE_FIELD_NUMBER: _ClassVar[int]
    PARAM1_FIELD_NUMBER: _ClassVar[int]
    PARAM2_FIELD_NUMBER: _ClassVar[int]
    PARAM3_FIELD_NUMBER: _ClassVar[int]
    PARAM4_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    broadcast: bool
    frame: int
    command: int
    current: int
    autocontinue: int
    param1: float
    param2: float
    param3: float
    param4: float
    x: int
    y: int
    z: float
    def __init__(self, broadcast: bool = ..., frame: _Optional[int] = ..., command: _Optional[int] = ..., current: _Optional[int] = ..., autocontinue: _Optional[int] = ..., param1: _Optional[float] = ..., param2: _Optional[float] = ..., param3: _Optional[float] = ..., param4: _Optional[float] = ..., x: _Optional[int] = ..., y: _Optional[int] = ..., z: _Optional[float] = ...) -> None: ...

class CommandIntResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
