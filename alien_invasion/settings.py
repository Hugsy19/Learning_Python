class Settings:
    """存储游戏设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        self.screen_width = 1200  # 屏幕大小
        self.screen_height = 800
        self.bg_color = (230, 230, 230)  # 背景颜色

        # 飞船设置
        self.ship_limit = 3  # 数量

        # 子弹设置
        self.bullet_width = 3  # 大小
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)  # 颜色
        self.bullets_allowed = 3  # 数量

        # 外星人设置
        self.fleet_drop_speed = 10  # 下落速度

        # 调整游戏难度
        self.speedup_scale = 1.1 # 节奏加快速度
        self.score_scale = 1.5 # 得分的倍数

        self.initialize_dynamic_settings()  # 动态设置

    def initialize_dynamic_settings(self):
        """随游戏进行而变化的设置"""
        self.ship_speed = 1.5  # 飞船速度
        self.bullet_speed = 3.0  # 子弹速度
        self.alien_speed = 1.0  # 外星人速度
        self.alien_points = 50  # 击毙一个外星人的得分
        self.fleet_direction = 1  # 外星人移动方向

    def increase_speed(self):
        """按倍数提高各项设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)