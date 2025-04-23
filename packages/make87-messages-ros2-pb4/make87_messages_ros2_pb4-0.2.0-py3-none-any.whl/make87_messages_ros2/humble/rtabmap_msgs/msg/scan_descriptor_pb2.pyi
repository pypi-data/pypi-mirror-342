from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import global_descriptor_pb2 as _global_descriptor_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import laser_scan_pb2 as _laser_scan_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScanDescriptor(_message.Message):
    __slots__ = ["header", "ros2_header", "scan", "scan_cloud", "global_descriptor"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    SCAN_FIELD_NUMBER: _ClassVar[int]
    SCAN_CLOUD_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_DESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    scan: _laser_scan_pb2.LaserScan
    scan_cloud: _point_cloud2_pb2.PointCloud2
    global_descriptor: _global_descriptor_pb2.GlobalDescriptor
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., scan: _Optional[_Union[_laser_scan_pb2.LaserScan, _Mapping]] = ..., scan_cloud: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ..., global_descriptor: _Optional[_Union[_global_descriptor_pb2.GlobalDescriptor, _Mapping]] = ...) -> None: ...
