from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import sbas_service_pb2 as _sbas_service_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import sbas_status_flags_pb2 as _sbas_status_flags_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import sbas_sv_data_pb2 as _sbas_sv_data_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavSBAS(_message.Message):
    __slots__ = ("header", "itow", "geo", "mode", "sys", "service", "cnt", "status_flags", "reserved_0", "sv_data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    GEO_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    SYS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    CNT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FLAGS_FIELD_NUMBER: _ClassVar[int]
    RESERVED_0_FIELD_NUMBER: _ClassVar[int]
    SV_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    itow: int
    geo: int
    mode: int
    sys: int
    service: _sbas_service_pb2.SBASService
    cnt: int
    status_flags: _sbas_status_flags_pb2.SBASStatusFlags
    reserved_0: _containers.RepeatedScalarFieldContainer[int]
    sv_data: _containers.RepeatedCompositeFieldContainer[_sbas_sv_data_pb2.SBASSvData]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., itow: _Optional[int] = ..., geo: _Optional[int] = ..., mode: _Optional[int] = ..., sys: _Optional[int] = ..., service: _Optional[_Union[_sbas_service_pb2.SBASService, _Mapping]] = ..., cnt: _Optional[int] = ..., status_flags: _Optional[_Union[_sbas_status_flags_pb2.SBASStatusFlags, _Mapping]] = ..., reserved_0: _Optional[_Iterable[int]] = ..., sv_data: _Optional[_Iterable[_Union[_sbas_sv_data_pb2.SBASSvData, _Mapping]]] = ...) -> None: ...
