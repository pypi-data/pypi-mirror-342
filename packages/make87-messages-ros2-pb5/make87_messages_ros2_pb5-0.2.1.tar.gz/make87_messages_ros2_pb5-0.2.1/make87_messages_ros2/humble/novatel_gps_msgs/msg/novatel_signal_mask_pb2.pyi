from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelSignalMask(_message.Message):
    __slots__ = ("header", "original_mask", "gps_l1_used_in_solution", "gps_l2_used_in_solution", "gps_l3_used_in_solution", "glonass_l1_used_in_solution", "glonass_l2_used_in_solution")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_MASK_FIELD_NUMBER: _ClassVar[int]
    GPS_L1_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    GPS_L2_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    GPS_L3_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    GLONASS_L1_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    GLONASS_L2_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    original_mask: int
    gps_l1_used_in_solution: bool
    gps_l2_used_in_solution: bool
    gps_l3_used_in_solution: bool
    glonass_l1_used_in_solution: bool
    glonass_l2_used_in_solution: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., original_mask: _Optional[int] = ..., gps_l1_used_in_solution: bool = ..., gps_l2_used_in_solution: bool = ..., gps_l3_used_in_solution: bool = ..., glonass_l1_used_in_solution: bool = ..., glonass_l2_used_in_solution: bool = ...) -> None: ...
