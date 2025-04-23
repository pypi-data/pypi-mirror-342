from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PVTGeodetic(_message.Message):
    __slots__ = ("header", "ros2_header", "block_header", "mode", "error", "latitude", "longitude", "height", "undulation", "vn", "ve", "vu", "cog", "rx_clk_bias", "rx_clk_drift", "time_system", "datum", "nr_sv", "wa_corr_info", "reference_id", "mean_corr_age", "signal_info", "alert_flag", "nr_bases", "ppp_info", "latency", "h_accuracy", "v_accuracy", "misc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    UNDULATION_FIELD_NUMBER: _ClassVar[int]
    VN_FIELD_NUMBER: _ClassVar[int]
    VE_FIELD_NUMBER: _ClassVar[int]
    VU_FIELD_NUMBER: _ClassVar[int]
    COG_FIELD_NUMBER: _ClassVar[int]
    RX_CLK_BIAS_FIELD_NUMBER: _ClassVar[int]
    RX_CLK_DRIFT_FIELD_NUMBER: _ClassVar[int]
    TIME_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    DATUM_FIELD_NUMBER: _ClassVar[int]
    NR_SV_FIELD_NUMBER: _ClassVar[int]
    WA_CORR_INFO_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
    MEAN_CORR_AGE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_INFO_FIELD_NUMBER: _ClassVar[int]
    ALERT_FLAG_FIELD_NUMBER: _ClassVar[int]
    NR_BASES_FIELD_NUMBER: _ClassVar[int]
    PPP_INFO_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    H_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    V_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    MISC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    block_header: _block_header_pb2.BlockHeader
    mode: int
    error: int
    latitude: float
    longitude: float
    height: float
    undulation: float
    vn: float
    ve: float
    vu: float
    cog: float
    rx_clk_bias: float
    rx_clk_drift: float
    time_system: int
    datum: int
    nr_sv: int
    wa_corr_info: int
    reference_id: int
    mean_corr_age: int
    signal_info: int
    alert_flag: int
    nr_bases: int
    ppp_info: int
    latency: int
    h_accuracy: int
    v_accuracy: int
    misc: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., mode: _Optional[int] = ..., error: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., height: _Optional[float] = ..., undulation: _Optional[float] = ..., vn: _Optional[float] = ..., ve: _Optional[float] = ..., vu: _Optional[float] = ..., cog: _Optional[float] = ..., rx_clk_bias: _Optional[float] = ..., rx_clk_drift: _Optional[float] = ..., time_system: _Optional[int] = ..., datum: _Optional[int] = ..., nr_sv: _Optional[int] = ..., wa_corr_info: _Optional[int] = ..., reference_id: _Optional[int] = ..., mean_corr_age: _Optional[int] = ..., signal_info: _Optional[int] = ..., alert_flag: _Optional[int] = ..., nr_bases: _Optional[int] = ..., ppp_info: _Optional[int] = ..., latency: _Optional[int] = ..., h_accuracy: _Optional[int] = ..., v_accuracy: _Optional[int] = ..., misc: _Optional[int] = ...) -> None: ...
