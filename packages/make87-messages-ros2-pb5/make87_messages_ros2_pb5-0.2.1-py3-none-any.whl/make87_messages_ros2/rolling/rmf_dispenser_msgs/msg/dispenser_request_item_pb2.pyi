from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DispenserRequestItem(_message.Message):
    __slots__ = ("type_guid", "quantity", "compartment_name")
    TYPE_GUID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    COMPARTMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    type_guid: str
    quantity: int
    compartment_name: str
    def __init__(self, type_guid: _Optional[str] = ..., quantity: _Optional[int] = ..., compartment_name: _Optional[str] = ...) -> None: ...
