# from launch import LaunchDescription
# from launch_ros.actions import Node

# # def generate_launch_description():
# #     return LaunchDescription([
# #         Node(
# #             package='cw1_team_2',
# #             executable='obstacle_follower',
# #             name='obstacle_follower',
# #             output='screen'
# #         )
# #     ])


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction, TimerAction
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():
    # Declare the use_sim_time argument
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',  # Default to true for simulation time
        description='Use simulation (Gazebo) clock if true'
    )

    declare_gazebo_world = DeclareLaunchArgument(
        'gazebo_world',
        default_value='world_1',
        description='Path to the Gazebo world file'
    )

    # Get the use_sim_time configuration to pass to nodes and included launch files
    use_sim_time = LaunchConfiguration("use_sim_time")
    gazebo_world = LaunchConfiguration("gazebo_world")

    # ros2 launch go2_config gazebo_mid360.launch.py
    gazebo_launch = IncludeLaunchDescription(
        # PythonLaunchDescriptionSource("gazebo_mid360_cw1.launch.py"),

        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("cw1_team_2"),
                'launch',
                'gazebo_mid360_cw1.launch.py'
            )
        ),
        launch_arguments={'use_sim_time': use_sim_time,
                          'gazebo_world': gazebo_world,
                        # 'world_init_x': '-1.0',    # 你想要的新默认值
                        # 'world_init_y': '-3.0',
                        # 'world_init_z': '0.5',
                        # 'world_init_heading': '1.57'
        }.items()  # Pass sim_time
    )

    # ros2 launch fast_lio mapping.launch.py
    mapping_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("fast_lio"),
            'launch',
            'mapping.launch.py'
            )
        ),
        launch_arguments={'config_file': 'unitree_go2_mid360.yaml', 'use_sim_time': use_sim_time}.items()
    )

    # ros2 run waypoint_follower waypoint_follower
    waypoint_follower_node = Node(
        package='cw1_team_2',
        executable='cw1_waypoint_follower',
        output='screen',
        parameters=[{"use_sim_time": use_sim_time}]
    )
    
    # ros2 run local_map_creator local_map_creator
    local_map_node = Node(
        package='local_map_creator',
        executable='local_map_creator',
        output='screen',
        parameters=[{"use_sim_time": use_sim_time}]
    )

    # ros2 run static_tf_node to connect the robot with the camera
    static_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '1.57', '0', '0', 'odom', 'body'],
        output='screen',
        parameters=[{"use_sim_time": use_sim_time}]
    )

    # segment groups
    gazebo_group = GroupAction([
        gazebo_launch
    ])
    mapping_group = GroupAction([
        mapping_launch
    ])
    local_map_group = GroupAction([
        local_map_node
    ])
    static_tf_group = GroupAction([
        static_tf_node
    ])
    waypoint_follower_group = GroupAction([
        waypoint_follower_node
    ])

    return LaunchDescription([
        declare_use_sim_time,  # Declare use_sim_time
        declare_gazebo_world,
        gazebo_group,
        mapping_group,
        local_map_group,
        static_tf_group,
        waypoint_follower_group,
    ])



# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction, TimerAction
# from launch.substitutions import LaunchConfiguration
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from ament_index_python.packages import get_package_share_directory
# from launch_ros.actions import Node
# import os

# def generate_launch_description():
#     # Declare the use_sim_time argument
#     declare_use_sim_time = DeclareLaunchArgument(
#         'use_sim_time',
#         default_value='true',  # Default to true for simulation time
#         description='Use simulation (Gazebo) clock if true'
#     )

#     # Get the use_sim_time configuration to pass to nodes and included launch files
#     use_sim_time = LaunchConfiguration("use_sim_time")

#     # ros2 launch go2_config gazebo_mid360.launch.py
#     gazebo_launch = IncludeLaunchDescription(
#         PythonLaunchDescriptionSource(
#             os.path.join(
#                 get_package_share_directory("go2_config"),
#                 'launch',
#                 'gazebo_mid360.launch.py'
#             )
#         ),
#         launch_arguments={'use_sim_time': use_sim_time,
#                         # 'world_init_x': '-1.0',    # 你想要的新默认值
#                         # 'world_init_y': '-3.0',
#                         # 'world_init_z': '0.5',
#                         # 'world_init_heading': '1.57'
#         }.items()  # Pass sim_time
#     )

#     # ros2 launch fast_lio mapping.launch.py
#     mapping_launch = IncludeLaunchDescription(
#         PythonLaunchDescriptionSource(
#             os.path.join(get_package_share_directory("fast_lio"),
#             'launch',
#             'mapping.launch.py'
#             )
#         ),
#         launch_arguments={'config_file': 'unitree_go2_mid360.yaml', 'use_sim_time': use_sim_time}.items()
#     )

#     # ros2 run waypoint_follower waypoint_follower
#     waypoint_follower_node = Node(
#         package='cw1_team_2',
#         executable='cw1_waypoint_follower',
#         output='screen',
#         parameters=[{"use_sim_time": use_sim_time}]
#     )
    
#     # ros2 run local_map_creator local_map_creator
#     local_map_node = Node(
#         package='local_map_creator',
#         executable='local_map_creator',
#         output='screen',
#         parameters=[{"use_sim_time": use_sim_time}]
#     )

#     # ros2 run static_tf_node to connect the robot with the camera
#     static_tf_node = Node(
#         package='tf2_ros',
#         executable='static_transform_publisher',
#         arguments=['0', '0', '0', '1.57', '0', '0', 'odom', 'body'],
#         output='screen',
#         parameters=[{"use_sim_time": use_sim_time}]
#     )

#     # segment groups
#     gazebo_group = GroupAction([
#         gazebo_launch
#     ])
#     mapping_group = GroupAction([
#         mapping_launch
#     ])
#     local_map_group = GroupAction([
#         local_map_node
#     ])
#     static_tf_group = GroupAction([
#         static_tf_node
#     ])
#     waypoint_follower_group = GroupAction([
#         waypoint_follower_node
#     ])

#     return LaunchDescription([
#         declare_use_sim_time,  # Declare use_sim_time
#         gazebo_group,
#         mapping_group,
#         local_map_group,
#         static_tf_group,
#         waypoint_follower_group
#     ])


