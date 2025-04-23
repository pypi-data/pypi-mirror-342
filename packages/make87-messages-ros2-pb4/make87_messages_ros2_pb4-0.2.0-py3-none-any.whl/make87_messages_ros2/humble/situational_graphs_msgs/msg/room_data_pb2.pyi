from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.situational_graphs_msgs.msg import plane_data_pb2 as _plane_data_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.visualization_msgs.msg import marker_array_pb2 as _marker_array_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RoomData(_message.Message):
    __slots__ = ["header", "ros2_header", "id", "neighbour_ids", "room_length", "room_center", "cluster_center", "x_planes", "y_planes", "planes", "cluster_array"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NEIGHBOUR_IDS_FIELD_NUMBER: _ClassVar[int]
    ROOM_LENGTH_FIELD_NUMBER: _ClassVar[int]
    ROOM_CENTER_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_CENTER_FIELD_NUMBER: _ClassVar[int]
    X_PLANES_FIELD_NUMBER: _ClassVar[int]
    Y_PLANES_FIELD_NUMBER: _ClassVar[int]
    PLANES_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ARRAY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    id: int
    neighbour_ids: _containers.RepeatedScalarFieldContainer[int]
    room_length: _point_pb2.Point
    room_center: _pose_pb2.Pose
    cluster_center: _point_pb2.Point
    x_planes: _containers.RepeatedCompositeFieldContainer[_plane_data_pb2.PlaneData]
    y_planes: _containers.RepeatedCompositeFieldContainer[_plane_data_pb2.PlaneData]
    planes: _containers.RepeatedCompositeFieldContainer[_plane_data_pb2.PlaneData]
    cluster_array: _marker_array_pb2.MarkerArray
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., id: _Optional[int] = ..., neighbour_ids: _Optional[_Iterable[int]] = ..., room_length: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., room_center: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., cluster_center: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., x_planes: _Optional[_Iterable[_Union[_plane_data_pb2.PlaneData, _Mapping]]] = ..., y_planes: _Optional[_Iterable[_Union[_plane_data_pb2.PlaneData, _Mapping]]] = ..., planes: _Optional[_Iterable[_Union[_plane_data_pb2.PlaneData, _Mapping]]] = ..., cluster_array: _Optional[_Union[_marker_array_pb2.MarkerArray, _Mapping]] = ...) -> None: ...
