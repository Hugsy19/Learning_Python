import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船及其初始位置
        :param ai_game: AlienInvasion对象
        """
        super().__init__()  # 初始化父类Sprite
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()  # 获取屏幕属性

        self.image = pygame.image.load("image/ship.bmp")  # 加载飞船
        self.rect = self.image.get_rect()  # 获取飞船属性

        self.center_ship()

        self.moving_left = False  # 移动标志
        self.moving_right = False

    def center_ship(self):
        """居中飞船"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)  # 获取飞船属性中的x值

    def blitme(self):
        """绘制飞船"""
        self.screen.blit(self.image, self.rect)  # 绘制

    def update(self):
        """移动飞船"""
        if self.moving_left and self.rect.left > 0:  # 防止越界
            self.x -= self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        self.rect.x = self.x  # 更新位置
