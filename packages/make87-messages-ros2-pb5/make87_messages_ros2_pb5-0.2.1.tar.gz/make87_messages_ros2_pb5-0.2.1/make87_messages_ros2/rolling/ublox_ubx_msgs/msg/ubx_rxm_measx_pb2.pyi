from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import measx_data_pb2 as _measx_data_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXRxmMeasx(_message.Message):
    __slots__ = ("header", "version", "gps_tow", "glo_tow", "bds_tow", "qzss_tow", "gps_tow_acc", "glo_tow_acc", "bds_tow_acc", "qzss_tow_acc", "num_sv", "flags", "sv_data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    GPS_TOW_FIELD_NUMBER: _ClassVar[int]
    GLO_TOW_FIELD_NUMBER: _ClassVar[int]
    BDS_TOW_FIELD_NUMBER: _ClassVar[int]
    QZSS_TOW_FIELD_NUMBER: _ClassVar[int]
    GPS_TOW_ACC_FIELD_NUMBER: _ClassVar[int]
    GLO_TOW_ACC_FIELD_NUMBER: _ClassVar[int]
    BDS_TOW_ACC_FIELD_NUMBER: _ClassVar[int]
    QZSS_TOW_ACC_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    SV_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    gps_tow: int
    glo_tow: int
    bds_tow: int
    qzss_tow: int
    gps_tow_acc: int
    glo_tow_acc: int
    bds_tow_acc: int
    qzss_tow_acc: int
    num_sv: int
    flags: int
    sv_data: _containers.RepeatedCompositeFieldContainer[_measx_data_pb2.MeasxData]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., gps_tow: _Optional[int] = ..., glo_tow: _Optional[int] = ..., bds_tow: _Optional[int] = ..., qzss_tow: _Optional[int] = ..., gps_tow_acc: _Optional[int] = ..., glo_tow_acc: _Optional[int] = ..., bds_tow_acc: _Optional[int] = ..., qzss_tow_acc: _Optional[int] = ..., num_sv: _Optional[int] = ..., flags: _Optional[int] = ..., sv_data: _Optional[_Iterable[_Union[_measx_data_pb2.MeasxData, _Mapping]]] = ...) -> None: ...
