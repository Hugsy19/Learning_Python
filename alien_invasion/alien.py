import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """管理外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人
        :param ai_game: AlienInvasion对象
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('image/alien.bmp')  # 加载外星人
        self.rect = self.image.get_rect()  # 获取外星人属性

        self.rect.x = self.rect.width  # 放在屏幕左上角
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        """更新外星人位置"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """检查外星人是否处于边界"""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= self.screen_rect.left:
            return True
