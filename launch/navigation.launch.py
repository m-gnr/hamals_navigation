import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    """HAMALS Nav2 (navigation-only) launch.

    Bu launch SADECE Nav2 navigation stack'ini başlatır.
    Aşağıdakiler kullanıcı tarafından MANUEL başlatılmalıdır:
      - hamals_serial_bridge (/odom + /cmd_vel relay)
      - hamals_localization (odom -> base_footprint TF + robot_state_publisher)
      - LiDAR driver (/scan)
      - hamals_slam (slam_toolbox localization: map -> odom)
    """

    # ------------------------------
    # Launch arguments
    # ------------------------------
    use_sim_time = LaunchConfiguration('use_sim_time')
    nav2_params_file = LaunchConfiguration('nav2_params_file')
    autostart = LaunchConfiguration('autostart')

    pkg_share = get_package_share_directory('hamals_navigation')
    nav2_params_default = os.path.join(pkg_share, 'config', 'nav2', 'nav2_params.yaml')

    # nav2_bringup navigation-only launch
    nav2_bringup_share = get_package_share_directory('nav2_bringup')
    nav2_navigation_launch = os.path.join(nav2_bringup_share, 'launch', 'navigation_launch.py')

    declare_args = [
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation clock if true.'
        ),
        DeclareLaunchArgument(
            'nav2_params_file',
            default_value=nav2_params_default,
            description='Path to Nav2 params yaml.'
        ),
        DeclareLaunchArgument(
            'autostart',
            default_value='true',
            description='Automatically transition Nav2 lifecycle nodes to active state.'
        ),
    ]

    nav2_navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_navigation_launch),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': nav2_params_file,
            'autostart': autostart,
        }.items(),
    )

    return LaunchDescription(declare_args + [nav2_navigation])