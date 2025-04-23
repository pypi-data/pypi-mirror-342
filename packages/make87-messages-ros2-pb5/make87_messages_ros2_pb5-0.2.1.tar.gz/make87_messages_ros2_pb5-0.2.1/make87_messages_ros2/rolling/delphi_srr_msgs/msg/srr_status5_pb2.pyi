from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SrrStatus5(_message.Message):
    __slots__ = ("header", "disable_auto_align", "can_tx_yaw_rate_ref_qf", "can_tx_yaw_rate_raw_qf", "can_tx_yaw_rate_reference", "can_tx_yaw_rate_raw", "can_tx_system_status", "can_tx_outside_temperature", "can_blockage_mnr_blocked", "can_blockage_bb_blocked", "can_blockage_radar_blocked", "can_td_blocked", "radar_tx_power_error", "radar_lo_power_error", "radar_data_sync_error", "linearizer_spi_transfer_error", "saturated_tuning_freq_error", "rtn_spi_transfer_error", "rrn_spi_transfer_error", "video_port_capture_error", "vertical_misalignment_error", "tx_temperature_fault", "transmitter_id_error", "dsp_unit_cal_checksum_error", "dsp_unit_cal_block_chcksm_error", "dsp_tuning_sensitivity_error", "dsp_loop_overrun_error", "adc_spi_transfer_error")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DISABLE_AUTO_ALIGN_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_YAW_RATE_REF_QF_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_YAW_RATE_RAW_QF_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_YAW_RATE_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_YAW_RATE_RAW_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_SYSTEM_STATUS_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_OUTSIDE_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    CAN_BLOCKAGE_MNR_BLOCKED_FIELD_NUMBER: _ClassVar[int]
    CAN_BLOCKAGE_BB_BLOCKED_FIELD_NUMBER: _ClassVar[int]
    CAN_BLOCKAGE_RADAR_BLOCKED_FIELD_NUMBER: _ClassVar[int]
    CAN_TD_BLOCKED_FIELD_NUMBER: _ClassVar[int]
    RADAR_TX_POWER_ERROR_FIELD_NUMBER: _ClassVar[int]
    RADAR_LO_POWER_ERROR_FIELD_NUMBER: _ClassVar[int]
    RADAR_DATA_SYNC_ERROR_FIELD_NUMBER: _ClassVar[int]
    LINEARIZER_SPI_TRANSFER_ERROR_FIELD_NUMBER: _ClassVar[int]
    SATURATED_TUNING_FREQ_ERROR_FIELD_NUMBER: _ClassVar[int]
    RTN_SPI_TRANSFER_ERROR_FIELD_NUMBER: _ClassVar[int]
    RRN_SPI_TRANSFER_ERROR_FIELD_NUMBER: _ClassVar[int]
    VIDEO_PORT_CAPTURE_ERROR_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_MISALIGNMENT_ERROR_FIELD_NUMBER: _ClassVar[int]
    TX_TEMPERATURE_FAULT_FIELD_NUMBER: _ClassVar[int]
    TRANSMITTER_ID_ERROR_FIELD_NUMBER: _ClassVar[int]
    DSP_UNIT_CAL_CHECKSUM_ERROR_FIELD_NUMBER: _ClassVar[int]
    DSP_UNIT_CAL_BLOCK_CHCKSM_ERROR_FIELD_NUMBER: _ClassVar[int]
    DSP_TUNING_SENSITIVITY_ERROR_FIELD_NUMBER: _ClassVar[int]
    DSP_LOOP_OVERRUN_ERROR_FIELD_NUMBER: _ClassVar[int]
    ADC_SPI_TRANSFER_ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    disable_auto_align: bool
    can_tx_yaw_rate_ref_qf: int
    can_tx_yaw_rate_raw_qf: int
    can_tx_yaw_rate_reference: float
    can_tx_yaw_rate_raw: float
    can_tx_system_status: int
    can_tx_outside_temperature: int
    can_blockage_mnr_blocked: bool
    can_blockage_bb_blocked: bool
    can_blockage_radar_blocked: bool
    can_td_blocked: bool
    radar_tx_power_error: bool
    radar_lo_power_error: bool
    radar_data_sync_error: bool
    linearizer_spi_transfer_error: bool
    saturated_tuning_freq_error: bool
    rtn_spi_transfer_error: bool
    rrn_spi_transfer_error: bool
    video_port_capture_error: bool
    vertical_misalignment_error: bool
    tx_temperature_fault: bool
    transmitter_id_error: bool
    dsp_unit_cal_checksum_error: bool
    dsp_unit_cal_block_chcksm_error: bool
    dsp_tuning_sensitivity_error: bool
    dsp_loop_overrun_error: bool
    adc_spi_transfer_error: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., disable_auto_align: bool = ..., can_tx_yaw_rate_ref_qf: _Optional[int] = ..., can_tx_yaw_rate_raw_qf: _Optional[int] = ..., can_tx_yaw_rate_reference: _Optional[float] = ..., can_tx_yaw_rate_raw: _Optional[float] = ..., can_tx_system_status: _Optional[int] = ..., can_tx_outside_temperature: _Optional[int] = ..., can_blockage_mnr_blocked: bool = ..., can_blockage_bb_blocked: bool = ..., can_blockage_radar_blocked: bool = ..., can_td_blocked: bool = ..., radar_tx_power_error: bool = ..., radar_lo_power_error: bool = ..., radar_data_sync_error: bool = ..., linearizer_spi_transfer_error: bool = ..., saturated_tuning_freq_error: bool = ..., rtn_spi_transfer_error: bool = ..., rrn_spi_transfer_error: bool = ..., video_port_capture_error: bool = ..., vertical_misalignment_error: bool = ..., tx_temperature_fault: bool = ..., transmitter_id_error: bool = ..., dsp_unit_cal_checksum_error: bool = ..., dsp_unit_cal_block_chcksm_error: bool = ..., dsp_tuning_sensitivity_error: bool = ..., dsp_loop_overrun_error: bool = ..., adc_spi_transfer_error: bool = ...) -> None: ...
