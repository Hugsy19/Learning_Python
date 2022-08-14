import pygame.font
from pygame.sprite import Group

from ship import Ship


class ScoreBoard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化各种属性
        :param ai_game: AlienInvasion对象
        """
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings  # 设置信息
        self.stats = ai_game.stats  # 状态信息

        self.text_color = (30, 30, 30)  # 字体颜色
        self.font = pygame.font.SysFont(None, 48)  # 字体

        self.prep_high_score()  # 初始化最高得分图像
        self.prep_score()  # 初始化得分图像
        self.prep_level()  # 初始化等级图像
        self.prep_ships()  # 初始化飞船数

    def prep_score(self):
        """将得分渲染为图像"""
        rounded_score = round(self.stats.score, -1)  # 舍入得分为10的倍数
        score_str = "{:,}".format(rounded_score)  # 用逗号分隔
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)  # 渲染为图像

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.high_score_rect.right  # 显示在右上角
        self.score_rect.top = self.high_score_rect.bottom + 10  # 最高得分下面

    def prep_high_score(self):
        """将最高分渲染为图像"""
        high_score = round(self.stats.high_score, -1)  # 舍入得分为10的倍数
        high_score_str = "{:,}".format(high_score)  # 用逗号分隔
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)  # 渲染为图像

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 20  # 显示在右上角
        self.high_score_rect.top = 20

    def prep_level(self):
        """将等级渲染为图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)  # 渲染为图像

        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.screen_rect.centerx  # 显示在中间
        self.level_rect.top = self.high_score_rect.top

    def prep_ships(self):
        """显示剩余飞船"""
        self.ships = Group()  # 编组
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """显示统计数据"""
        self.screen.blit(self.high_score_image, self.high_score_rect)  # 最高得分
        self.screen.blit(self.score_image, self.score_rect)  # 得分
        self.screen.blit(self.level_image, self.level_rect)  # 等级
        self.ships.draw(self.screen)  # 剩余飞船

    def check_high_score(self):
        """检查是否为最高得分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
