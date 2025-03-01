import numpy as np
from obstacle_follow import ObstacleFollower

class Robot:
    """带方向的可移动机器人，增加局部传感器 & 障碍物跟随"""

    def __init__(self, env, start_pos=(0.5, 0.5), start_angle=0, sensor_range=0.9, step_size=0.05):
        self.env = env
        self.position = np.array(start_pos)
        self.angle = start_angle  # 方向，以弧度表示
        self.sensor_range = sensor_range
        self.step_size = step_size  # 机器人步长
        self.path = [tuple(self.position)]  # 记录轨迹
        self.follower = ObstacleFollower(self)  # 绑定绕障行为

    def move_forward(self):
        """沿当前方向前进"""
        dx = self.step_size * np.cos(self.angle)
        dy = self.step_size * np.sin(self.angle)
        new_pos = self.position + np.array([dx, dy])

        # 仅当未撞上障碍物时更新位置
        if not self.env.is_collision(new_pos):
            self.position = new_pos
            self.path.append(tuple(self.position))

    def rotate(self, delta_angle):
        """旋转机器人"""
        self.angle += delta_angle  # 角度单位为弧度

    def get_local_obstacles(self):
        """获取局部感知到的障碍物点"""
        return self.env.get_obstacles_near(self.position, self.sensor_range)

    def navigate(self):
        """导航逻辑：检测障碍物 -> 决定绕障或前进"""
        nearest_obs = self.follower.check_if_near_obstacle()
        
        if nearest_obs is not None:
            self.follower.follow_obstacle()  # 触发绕障
        else:
            self.move_forward()  # 机器人前进
            self.rotate(0.01)  # 每步旋转 0.1 弧度
