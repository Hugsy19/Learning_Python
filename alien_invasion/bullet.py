import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):  # 继承Sprite类，方便元素编组
    """管理飞船所发射子弹的类"""

    def __init__(self, ai_game):
        """初始化子弹
        :param ai_game: AlienInvasion对象
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)  # 创建子弹
        self.rect.midtop = ai_game.ship.rect.midtop  # 设置位置

        self.y = float(self.rect.y)

    def update(self):
        """移动子弹"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
