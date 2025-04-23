from make87_messages_ros2.rolling.ibeo_msgs.msg import contour_point_sigma_pb2 as _contour_point_sigma_pb2
from make87_messages_ros2.rolling.ibeo_msgs.msg import point2_di_pb2 as _point2_di_pb2
from make87_messages_ros2.rolling.ibeo_msgs.msg import point2_dui_pb2 as _point2_dui_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UntrackedProperties(_message.Message):
    __slots__ = ("relative_time_of_measurement", "position_closest_point", "object_box_size", "object_box_size_sigma", "object_box_orientation", "object_box_orientation_sigma", "tracking_point_coordinate", "tracking_point_coordinate_sigma", "number_of_contour_points", "contour_point_list")
    RELATIVE_TIME_OF_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    POSITION_CLOSEST_POINT_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_SIZE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_SIZE_SIGMA_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_ORIENTATION_SIGMA_FIELD_NUMBER: _ClassVar[int]
    TRACKING_POINT_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    TRACKING_POINT_COORDINATE_SIGMA_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_CONTOUR_POINTS_FIELD_NUMBER: _ClassVar[int]
    CONTOUR_POINT_LIST_FIELD_NUMBER: _ClassVar[int]
    relative_time_of_measurement: int
    position_closest_point: _point2_di_pb2.Point2Di
    object_box_size: _point2_di_pb2.Point2Di
    object_box_size_sigma: _point2_dui_pb2.Point2Dui
    object_box_orientation: int
    object_box_orientation_sigma: int
    tracking_point_coordinate: _point2_di_pb2.Point2Di
    tracking_point_coordinate_sigma: _point2_dui_pb2.Point2Dui
    number_of_contour_points: int
    contour_point_list: _containers.RepeatedCompositeFieldContainer[_contour_point_sigma_pb2.ContourPointSigma]
    def __init__(self, relative_time_of_measurement: _Optional[int] = ..., position_closest_point: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., object_box_size: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., object_box_size_sigma: _Optional[_Union[_point2_dui_pb2.Point2Dui, _Mapping]] = ..., object_box_orientation: _Optional[int] = ..., object_box_orientation_sigma: _Optional[int] = ..., tracking_point_coordinate: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., tracking_point_coordinate_sigma: _Optional[_Union[_point2_dui_pb2.Point2Dui, _Mapping]] = ..., number_of_contour_points: _Optional[int] = ..., contour_point_list: _Optional[_Iterable[_Union[_contour_point_sigma_pb2.ContourPointSigma, _Mapping]]] = ...) -> None: ...
