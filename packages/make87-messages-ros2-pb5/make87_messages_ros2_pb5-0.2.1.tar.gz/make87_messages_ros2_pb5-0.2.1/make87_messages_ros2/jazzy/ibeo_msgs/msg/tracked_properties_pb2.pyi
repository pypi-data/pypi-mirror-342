from make87_messages_ros2.jazzy.ibeo_msgs.msg import contour_point_sigma_pb2 as _contour_point_sigma_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import point2_di_pb2 as _point2_di_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import point2_dui_pb2 as _point2_dui_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrackedProperties(_message.Message):
    __slots__ = ("object_age", "hidden_status_age", "object_phase", "dynamic_property", "relative_time_of_measure", "position_closest_point", "relative_velocity", "relative_velocity_sigma", "classification", "classification_age", "object_box_size", "object_box_size_sigma", "object_box_orientation", "object_box_orientation_sigma", "tracking_point_location", "tracking_point_coordinate", "tracking_point_coordinate_sigma", "velocity", "velocity_sigma", "acceleration", "acceleration_sigma", "yaw_rate", "yaw_rate_sigma", "number_of_contour_points", "contour_point_list")
    OBJECT_AGE_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_STATUS_AGE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_PHASE_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_PROPERTY_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_TIME_OF_MEASURE_FIELD_NUMBER: _ClassVar[int]
    POSITION_CLOSEST_POINT_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_SIGMA_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_AGE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_SIZE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_SIZE_SIGMA_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_ORIENTATION_SIGMA_FIELD_NUMBER: _ClassVar[int]
    TRACKING_POINT_LOCATION_FIELD_NUMBER: _ClassVar[int]
    TRACKING_POINT_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    TRACKING_POINT_COORDINATE_SIGMA_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_SIGMA_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_SIGMA_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_SIGMA_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_CONTOUR_POINTS_FIELD_NUMBER: _ClassVar[int]
    CONTOUR_POINT_LIST_FIELD_NUMBER: _ClassVar[int]
    object_age: int
    hidden_status_age: int
    object_phase: int
    dynamic_property: int
    relative_time_of_measure: int
    position_closest_point: _point2_di_pb2.Point2Di
    relative_velocity: _point2_di_pb2.Point2Di
    relative_velocity_sigma: _point2_dui_pb2.Point2Dui
    classification: int
    classification_age: int
    object_box_size: _point2_di_pb2.Point2Di
    object_box_size_sigma: _point2_dui_pb2.Point2Dui
    object_box_orientation: int
    object_box_orientation_sigma: int
    tracking_point_location: int
    tracking_point_coordinate: _point2_di_pb2.Point2Di
    tracking_point_coordinate_sigma: _point2_dui_pb2.Point2Dui
    velocity: _point2_di_pb2.Point2Di
    velocity_sigma: _point2_dui_pb2.Point2Dui
    acceleration: _point2_di_pb2.Point2Di
    acceleration_sigma: _point2_dui_pb2.Point2Dui
    yaw_rate: int
    yaw_rate_sigma: int
    number_of_contour_points: int
    contour_point_list: _containers.RepeatedCompositeFieldContainer[_contour_point_sigma_pb2.ContourPointSigma]
    def __init__(self, object_age: _Optional[int] = ..., hidden_status_age: _Optional[int] = ..., object_phase: _Optional[int] = ..., dynamic_property: _Optional[int] = ..., relative_time_of_measure: _Optional[int] = ..., position_closest_point: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., relative_velocity: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., relative_velocity_sigma: _Optional[_Union[_point2_dui_pb2.Point2Dui, _Mapping]] = ..., classification: _Optional[int] = ..., classification_age: _Optional[int] = ..., object_box_size: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., object_box_size_sigma: _Optional[_Union[_point2_dui_pb2.Point2Dui, _Mapping]] = ..., object_box_orientation: _Optional[int] = ..., object_box_orientation_sigma: _Optional[int] = ..., tracking_point_location: _Optional[int] = ..., tracking_point_coordinate: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., tracking_point_coordinate_sigma: _Optional[_Union[_point2_dui_pb2.Point2Dui, _Mapping]] = ..., velocity: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., velocity_sigma: _Optional[_Union[_point2_dui_pb2.Point2Dui, _Mapping]] = ..., acceleration: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., acceleration_sigma: _Optional[_Union[_point2_dui_pb2.Point2Dui, _Mapping]] = ..., yaw_rate: _Optional[int] = ..., yaw_rate_sigma: _Optional[int] = ..., number_of_contour_points: _Optional[int] = ..., contour_point_list: _Optional[_Iterable[_Union[_contour_point_sigma_pb2.ContourPointSigma, _Mapping]]] = ...) -> None: ...
