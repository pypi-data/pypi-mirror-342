from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import transform_pb2 as _transform_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import env_sensor_pb2 as _env_sensor_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import global_descriptor_pb2 as _global_descriptor_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import gps_pb2 as _gps_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import key_point_pb2 as _key_point_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import landmark_detection_pb2 as _landmark_detection_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import point3f_pb2 as _point3f_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import camera_info_pb2 as _camera_info_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import image_pb2 as _image_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import imu_pb2 as _imu_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorData(_message.Message):
    __slots__ = ("header", "ros2_header", "left", "right", "left_compressed", "right_compressed", "left_camera_info", "right_camera_info", "local_transform", "laser_scan", "laser_scan_compressed", "laser_scan_max_pts", "laser_scan_max_range", "laser_scan_format", "laser_scan_local_transform", "user_data", "grid_ground", "grid_obstacles", "grid_empty_cells", "grid_cell_size", "grid_view_point", "key_points", "points", "descriptors", "global_descriptors", "env_sensors", "imu", "imu_local_transform", "landmarks", "ground_truth_pose", "gps")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    LEFT_COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    RIGHT_COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    LEFT_CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    RIGHT_CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    LOCAL_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    LASER_SCAN_FIELD_NUMBER: _ClassVar[int]
    LASER_SCAN_COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    LASER_SCAN_MAX_PTS_FIELD_NUMBER: _ClassVar[int]
    LASER_SCAN_MAX_RANGE_FIELD_NUMBER: _ClassVar[int]
    LASER_SCAN_FORMAT_FIELD_NUMBER: _ClassVar[int]
    LASER_SCAN_LOCAL_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    GRID_GROUND_FIELD_NUMBER: _ClassVar[int]
    GRID_OBSTACLES_FIELD_NUMBER: _ClassVar[int]
    GRID_EMPTY_CELLS_FIELD_NUMBER: _ClassVar[int]
    GRID_CELL_SIZE_FIELD_NUMBER: _ClassVar[int]
    GRID_VIEW_POINT_FIELD_NUMBER: _ClassVar[int]
    KEY_POINTS_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    ENV_SENSORS_FIELD_NUMBER: _ClassVar[int]
    IMU_FIELD_NUMBER: _ClassVar[int]
    IMU_LOCAL_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    LANDMARKS_FIELD_NUMBER: _ClassVar[int]
    GROUND_TRUTH_POSE_FIELD_NUMBER: _ClassVar[int]
    GPS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    left: _image_pb2.Image
    right: _image_pb2.Image
    left_compressed: _containers.RepeatedScalarFieldContainer[int]
    right_compressed: _containers.RepeatedScalarFieldContainer[int]
    left_camera_info: _containers.RepeatedCompositeFieldContainer[_camera_info_pb2.CameraInfo]
    right_camera_info: _containers.RepeatedCompositeFieldContainer[_camera_info_pb2.CameraInfo]
    local_transform: _containers.RepeatedCompositeFieldContainer[_transform_pb2.Transform]
    laser_scan: _point_cloud2_pb2.PointCloud2
    laser_scan_compressed: _containers.RepeatedScalarFieldContainer[int]
    laser_scan_max_pts: int
    laser_scan_max_range: float
    laser_scan_format: int
    laser_scan_local_transform: _transform_pb2.Transform
    user_data: _containers.RepeatedScalarFieldContainer[int]
    grid_ground: _containers.RepeatedScalarFieldContainer[int]
    grid_obstacles: _containers.RepeatedScalarFieldContainer[int]
    grid_empty_cells: _containers.RepeatedScalarFieldContainer[int]
    grid_cell_size: float
    grid_view_point: _point3f_pb2.Point3f
    key_points: _containers.RepeatedCompositeFieldContainer[_key_point_pb2.KeyPoint]
    points: _containers.RepeatedCompositeFieldContainer[_point3f_pb2.Point3f]
    descriptors: _containers.RepeatedScalarFieldContainer[int]
    global_descriptors: _containers.RepeatedCompositeFieldContainer[_global_descriptor_pb2.GlobalDescriptor]
    env_sensors: _containers.RepeatedCompositeFieldContainer[_env_sensor_pb2.EnvSensor]
    imu: _imu_pb2.Imu
    imu_local_transform: _transform_pb2.Transform
    landmarks: _containers.RepeatedCompositeFieldContainer[_landmark_detection_pb2.LandmarkDetection]
    ground_truth_pose: _pose_pb2.Pose
    gps: _gps_pb2.GPS
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., left: _Optional[_Union[_image_pb2.Image, _Mapping]] = ..., right: _Optional[_Union[_image_pb2.Image, _Mapping]] = ..., left_compressed: _Optional[_Iterable[int]] = ..., right_compressed: _Optional[_Iterable[int]] = ..., left_camera_info: _Optional[_Iterable[_Union[_camera_info_pb2.CameraInfo, _Mapping]]] = ..., right_camera_info: _Optional[_Iterable[_Union[_camera_info_pb2.CameraInfo, _Mapping]]] = ..., local_transform: _Optional[_Iterable[_Union[_transform_pb2.Transform, _Mapping]]] = ..., laser_scan: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ..., laser_scan_compressed: _Optional[_Iterable[int]] = ..., laser_scan_max_pts: _Optional[int] = ..., laser_scan_max_range: _Optional[float] = ..., laser_scan_format: _Optional[int] = ..., laser_scan_local_transform: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ..., user_data: _Optional[_Iterable[int]] = ..., grid_ground: _Optional[_Iterable[int]] = ..., grid_obstacles: _Optional[_Iterable[int]] = ..., grid_empty_cells: _Optional[_Iterable[int]] = ..., grid_cell_size: _Optional[float] = ..., grid_view_point: _Optional[_Union[_point3f_pb2.Point3f, _Mapping]] = ..., key_points: _Optional[_Iterable[_Union[_key_point_pb2.KeyPoint, _Mapping]]] = ..., points: _Optional[_Iterable[_Union[_point3f_pb2.Point3f, _Mapping]]] = ..., descriptors: _Optional[_Iterable[int]] = ..., global_descriptors: _Optional[_Iterable[_Union[_global_descriptor_pb2.GlobalDescriptor, _Mapping]]] = ..., env_sensors: _Optional[_Iterable[_Union[_env_sensor_pb2.EnvSensor, _Mapping]]] = ..., imu: _Optional[_Union[_imu_pb2.Imu, _Mapping]] = ..., imu_local_transform: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ..., landmarks: _Optional[_Iterable[_Union[_landmark_detection_pb2.LandmarkDetection, _Mapping]]] = ..., ground_truth_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., gps: _Optional[_Union[_gps_pb2.GPS, _Mapping]] = ...) -> None: ...
