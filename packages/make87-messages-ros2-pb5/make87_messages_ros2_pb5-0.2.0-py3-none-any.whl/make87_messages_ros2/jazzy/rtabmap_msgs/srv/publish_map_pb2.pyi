from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PublishMapRequest(_message.Message):
    __slots__ = ("global_map", "optimized", "graph_only")
    GLOBAL_MAP_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZED_FIELD_NUMBER: _ClassVar[int]
    GRAPH_ONLY_FIELD_NUMBER: _ClassVar[int]
    global_map: bool
    optimized: bool
    graph_only: bool
    def __init__(self, global_map: bool = ..., optimized: bool = ..., graph_only: bool = ...) -> None: ...

class PublishMapResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
