class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.game_active = False  # 是否结束
        self.high_score = 0  # 最高得分
        self.reset_stats()

    def reset_stats(self):
        """重置统计数据"""
        self.ships_left = self.settings.ship_limit  # 剩余飞船数
        self.score = 0  # 得分
        self.level = 1  # 游戏等级
