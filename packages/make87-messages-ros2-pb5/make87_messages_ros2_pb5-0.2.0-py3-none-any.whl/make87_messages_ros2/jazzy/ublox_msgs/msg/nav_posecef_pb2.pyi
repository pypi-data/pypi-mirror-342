from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavPOSECEF(_message.Message):
    __slots__ = ("i_tow", "ecef_x", "ecef_y", "ecef_z", "p_acc")
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    ECEF_X_FIELD_NUMBER: _ClassVar[int]
    ECEF_Y_FIELD_NUMBER: _ClassVar[int]
    ECEF_Z_FIELD_NUMBER: _ClassVar[int]
    P_ACC_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    ecef_x: int
    ecef_y: int
    ecef_z: int
    p_acc: int
    def __init__(self, i_tow: _Optional[int] = ..., ecef_x: _Optional[int] = ..., ecef_y: _Optional[int] = ..., ecef_z: _Optional[int] = ..., p_acc: _Optional[int] = ...) -> None: ...
