from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccEvent(_message.Message):
    __slots__ = ("event_type", "event_object_tag", "event_source", "label")
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENT_OBJECT_TAG_FIELD_NUMBER: _ClassVar[int]
    EVENT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    event_type: str
    event_object_tag: str
    event_source: str
    label: str
    def __init__(self, event_type: _Optional[str] = ..., event_object_tag: _Optional[str] = ..., event_source: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...
